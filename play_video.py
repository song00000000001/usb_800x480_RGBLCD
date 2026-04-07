#!/usr/bin/env python3
"""
ESP32-P4 USB 视频播放器
通过GStreamer解码MP4视频，通过USB发送帧到ESP32-P4显示
尽力发送模式 - 不等待，根据ESP32处理能力自适应
"""

import usb.core
import usb.util
import struct
import time
import sys
import argparse
import os
import numpy as np
import queue
from PIL import Image
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib

# 初始化GStreamer
Gst.init(None)

# USB设备参数
VID = 0x303a
PID = 0x2986

# 屏幕参数
WIDTH = 800
HEIGHT = 480

# 图像类型
UDISP_TYPE_RGB565 = 0
UDISP_TYPE_JPG = 3

# JPEG压缩质量 - 降低质量提高编码速度
JPEG_QUALITY = 20

# 全局变量
frame_queue = queue.Queue(maxsize=10)  # 增大队列避免丢帧
ep_out = None


def rgb565_convert(img):
    """快速RGB565转换"""
    pixels = np.array(img)
    r5 = (pixels[:,:,0] >> 3).astype(np.uint16)
    g6 = (pixels[:,:,1] >> 2).astype(np.uint16)
    b5 = (pixels[:,:,2] >> 3).astype(np.uint16)
    rgb565 = (r5 << 11) | (g6 << 5) | b5
    return rgb565.astype('<u2').tobytes()


def crc16(data):
    """计算CRC16校验"""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def create_frame_header(width, height, payload_size, frame_type, frame_id):
    """创建帧头"""
    SYNC_MARKER = b'UDSP'
    frame_id_payload = ((frame_id & 0x3FF) | ((payload_size & 0x3FFFFF) << 10))
    header_data = struct.pack('<BBHHHHI',
        frame_type, 0, 0, 0, width, height, frame_id_payload)
    crc = crc16(header_data)
    full_header = struct.pack('<H', crc) + header_data
    return SYNC_MARKER + full_header + bytes(512 - len(SYNC_MARKER) - len(full_header))


def find_usb_device():
    """查找并配置USB设备"""
    print(f"查找设备 VID=0x{VID:04x}, PID=0x{PID:04x}")
    dev = usb.core.find(idVendor=VID, idProduct=PID)
    if dev is None:
        print("未找到设备!")
        return None
    print(f"找到设备: {dev}")
    try:
        for cfg in dev:
            for intf in cfg:
                if dev.is_kernel_driver_active(intf.bInterfaceNumber):
                    try:
                        dev.detach_kernel_driver(intf.bInterfaceNumber)
                    except:
                        pass
        dev.set_configuration()
    except Exception as e:
        print(f"配置设备失败: {e}")
        return None
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]
    ep_out = usb.util.find_descriptor(
        intf,
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
    )
    if ep_out is None:
        print("未找到OUT端点!")
        return None
    print(f"OUT端点: 0x{ep_out.bEndpointAddress:02x}")
    return ep_out


def send_frame(img, frame_id):
    """发送一帧图像"""
    global ep_out

    if ep_out is None:
        return False, 0

    # 调整大小到屏幕尺寸
    if img.size != (WIDTH, HEIGHT):
        orig_w, orig_h = img.size
        scale = min(WIDTH / orig_w, HEIGHT / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

        if img.size != (WIDTH, HEIGHT):
            result = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
            paste_x = (WIDTH - new_w) // 2
            paste_y = (HEIGHT - new_h) // 2
            result.paste(img, (paste_x, paste_y))
            img = result

    # JPEG压缩
    import io
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=JPEG_QUALITY, optimize=False)
    data = buffer.getvalue()
    frame_type = UDISP_TYPE_JPG

    payload_size = len(data)
    header = create_frame_header(WIDTH, HEIGHT, payload_size, frame_type, frame_id)

    try:
        ep_out.write(header)
        chunk_size = 4096
        for offset in range(0, len(data), chunk_size):
            ep_out.write(data[offset:offset + chunk_size])
        return True, payload_size
    except usb.core.USBError as e:
        print(f"发送失败: {e}")
        return False, 0


class VideoPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.pipeline = None
        self.appsink = None
        self.eos = False
        self.frame_count = 0

    def create_pipeline(self):
        """创建视频解码管道 - sync=true让GStreamer按真实时间播放"""
        pipeline_str = (
            f'filesrc location="{os.path.abspath(self.video_path)}" ! '
            f'qtdemux name=demux ! '
            f'h264parse ! '
            f'avdec_h264 ! '
            f'videoconvert ! '
            f'video/x-raw,format=RGB ! '
            f'appsink name=sink emit-signals=true drop=true max-buffers=10 sync=true'
        )
        print(f"管道: {pipeline_str}")

        try:
            self.pipeline = Gst.parse_launch(pipeline_str)
            self.appsink = self.pipeline.get_by_name('sink')
            self.appsink.connect('new-sample', self._on_frame)

            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._on_message)

            return True
        except Exception as e:
            print(f"管道创建失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _on_frame(self, sink):
        """处理解码后的帧"""
        sample = sink.emit('pull-sample')
        if sample:
            buf = sample.get_buffer()
            ok, info = buf.map(Gst.MapFlags.READ)
            if ok:
                try:
                    caps = sample.get_caps()
                    if caps:
                        structure = caps.get_structure(0)
                        frame_w = structure.get_value('width')
                        frame_h = structure.get_value('height')
                        if structure.has_field('stride'):
                            stride = structure.get_value('stride')
                        else:
                            stride = frame_w * 3
                    else:
                        frame_w, frame_h, stride = WIDTH, HEIGHT, WIDTH * 3

                    # 提取RGB数据
                    data = np.frombuffer(info.data, dtype=np.uint8)
                    lines = []
                    for y in range(frame_h):
                        offset = y * stride
                        line_data = data[offset:offset + frame_w * 3]
                        lines.append(line_data)
                    img_data = np.concatenate(lines)

                    if len(img_data) == frame_w * frame_h * 3:
                        img = Image.fromarray(
                            img_data.reshape((frame_h, frame_w, 3)).astype(np.uint8)
                        )

                        if frame_queue.full():
                            try:
                                frame_queue.get_nowait()  # 丢弃旧帧
                            except:
                                pass
                        try:
                            frame_queue.put_nowait(img)
                        except:
                            pass
                        self.frame_count += 1
                except Exception as e:
                    print(f"帧处理错误: {e}")
                buf.unmap(info)
        return Gst.FlowReturn.OK

    def _on_message(self, bus, msg):
        if msg.type == Gst.MessageType.EOS:
            print("\n视频播放完成!")
            self.eos = True
        elif msg.type == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            print(f"GStreamer错误: {err}")

    def play(self):
        """启动播放"""
        if not self.create_pipeline():
            return False

        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("播放启动失败")
            return False

        print("开始播放...")
        return True

    def stop(self):
        """停止播放"""
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)


def main():
    parser = argparse.ArgumentParser(description='ESP32-P4 视频播放器')
    parser.add_argument('video', help='视频文件路径')
    parser.add_argument('--loop', action='store_true', help='循环播放')
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"视频文件不存在: {args.video}")
        return

    print("=" * 50)
    print("ESP32-P4 视频播放器")
    print(f"视频文件: {args.video}")
    print(f"JPEG质量: {JPEG_QUALITY}")
    print("=" * 50)

    global ep_out
    ep_out = find_usb_device()
    if not ep_out:
        return

    player = VideoPlayer(args.video)

    loop = GLib.MainLoop()
    frame_id = 0
    last = time.time()
    count = 0
    total = 0
    start_time = time.time()
    player_playing = [True]  # 使用列表以便在嵌套函数中修改

    def check_failed():
        """检查是否启动失败或播放结束"""
        if player.eos:
            if args.loop:
                print("\n循环播放...")
                player.stop()
                player.__init__(args.video)  # 重新初始化
                if not player.play():
                    loop.quit()
                    return False
            else:
                loop.quit()
                return False
        return True

    if not player.play():
        return

    # 限制发送帧率 - ESP32 JPEG解码约30-60fps，根据实际情况调整
    target_fps = 24
    frame_interval = 1.0 / target_fps
    last_send_time = [0.0]

    def send_frame_callback():
        """尽力发送帧 - 限制帧率"""
        nonlocal frame_id, total, last, count

        now = time.time()
        # 限制帧率
        if now - last_send_time[0] < frame_interval:
            return True
        last_send_time[0] = now

        try:
            img = frame_queue.get_nowait()
            ok, size = send_frame(img, frame_id)
            if ok:
                total += size
                count += 1
                frame_id += 1

            if now - last >= 1.0:
                elapsed = now - start_time
                fps = count / (now - last)
                bitrate = total * 8 / (now - last) / 1000
                queue_size = frame_queue.qsize()
                print(f"FPS: {fps:.1f} | 带宽: {bitrate:.0f}kbps | 帧: {frame_id} | 视频: {elapsed:.1f}s | 队列: {queue_size}")
                last = now
                count = 0
                total = 0
        except queue.Empty:
            pass

        return True

    # 高频率检查队列
    GLib.timeout_add(16, send_frame_callback)  # ~60fps
    GLib.timeout_add(200, check_failed)

    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    print(f"\n播放结束 - 总帧数: {frame_id}")
    player.stop()


if __name__ == '__main__':
    main()
