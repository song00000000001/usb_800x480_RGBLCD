#!/usr/bin/env python3
"""
ESP32-P4 USB 音频播放器
通过GStreamer解码MP4音频，发送至ESP32-P4播放
"""

import sys
import os
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib

# 初始化GStreamer
Gst.init(None)

# 音频参数 (必须与app_uac.c中的UAC参数匹配)
SAMPLE_RATE = 24000
CHANNELS = 1
BIT_WIDTH = 16
BYTES_PER_SAMPLE = BIT_WIDTH // 8
FRAME_SIZE = 480  # 10ms interval * 24000Hz * 1ch * 2bytes = 480 bytes


class AudioPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.pipeline = None
        self.appsink = None
        self.eos = False
        self.frame_count = 0

    def create_pipeline(self):
        """创建音频解码管道"""
        # 使用 decodebin3 自动处理音频解码和输出
        pipeline_str = (
            f'filesrc location="{os.path.abspath(self.video_path)}" ! '
            f'decodebin3 name=db ! '
            f'audioconvert ! '
            f'audio/x-raw,rate={SAMPLE_RATE},channels={CHANNELS},format=S16LE ! '
            f'appsink name=sink emit-signals=true drop=true max-buffers=50'
        )
        print(f"音频管道: {pipeline_str}")

        try:
            self.pipeline = Gst.parse_launch(pipeline_str)

            # 获取appsink
            self.appsink = self.pipeline.get_by_name('sink')
            if self.appsink:
                self.appsink.connect('new-sample', self._on_audio)

            # 获取bus并添加信号监听
            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._on_message)

            return True
        except Exception as e:
            print(f"管道创建失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _on_audio(self, sink):
        """处理解码后的音频"""
        sample = sink.emit('pull-sample')
        if sample:
            buf = sample.get_buffer()
            ok, info = buf.map(Gst.MapFlags.READ)
            if ok:
                try:
                    data = bytes(info.data)
                    self.frame_count += 1
                    buf.unmap(info)
                    return data
                except Exception as e:
                    print(f"音频处理错误: {e}")
                    buf.unmap(info)
        return None

    def _on_message(self, bus, msg):
        if msg.type == Gst.MessageType.EOS:
            print("\n音频播放完成!")
            self.eos = True
        elif msg.type == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            print(f"GStreamer错误: {err}")
        elif msg.type == Gst.MessageType.WARNING:
            warn, dbg = msg.parse_warning()
            print(f"GStreamer警告: {warn}")

    def play(self):
        """启动播放"""
        if not self.create_pipeline():
            return False

        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("播放启动失败")
            return False

        print("开始音频播放...")
        return True

    def stop(self):
        """停止播放"""
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)


def main():
    if len(sys.argv) < 2:
        video_path = "/home/nini/airi_esp32p4/4.3/usb_800x480_RGBLCD/Retro Anime - Detective Conan (2000) [2040852006185709568].mp4"
    else:
        video_path = sys.argv[1]

    if not os.path.exists(video_path):
        print(f"视频文件不存在: {video_path}")
        return

    print("=" * 50)
    print("ESP32-P4 音频播放器")
    print(f"音频文件: {video_path}")
    print(f"采样率: {SAMPLE_RATE} Hz")
    print(f"通道数: {CHANNELS}")
    print(f"位宽: {BIT_WIDTH} bit")
    print("=" * 50)

    player = AudioPlayer(video_path)

    loop = GLib.MainLoop()
    last = time.time()
    count = 0
    start_time = time.time()

    def check_failed():
        if player.eos:
            loop.quit()
            return False
        return True

    if not player.play():
        return

    def process_audio_callback():
        """处理并输出音频"""
        nonlocal count, last, start_time

        if player.appsink:
            sample = player.appsink.emit('pull-sample')
            if sample:
                buf = sample.get_buffer()
                ok, info = buf.map(Gst.MapFlags.READ)
                if ok:
                    data = bytes(info.data)
                    # 音频数据在 player.frame_count 中计数
                    buf.unmap(info)

                    now = time.time()
                    if now - last >= 1.0:
                        elapsed = now - start_time
                        fps = count / (now - last) if (now - last) > 0 else 0
                        print(f"音频帧: {count} | 帧率: {fps:.1f} fps | 时间: {elapsed:.1f}s")
                        last = now
                        count = 0

        return True

    # 较高频率检查音频 (~100fps)
    GLib.timeout_add(10, process_audio_callback)
    GLib.timeout_add(500, check_failed)

    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    print(f"\n播放结束 - 总音频帧: {player.frame_count}")
    player.stop()


if __name__ == '__main__':
    import time
    main()