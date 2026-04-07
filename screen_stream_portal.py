#!/usr/bin/env python3
"""
ESP32-P4 USB 屏幕投屏脚本 - Portal ScreenCast版本
使用Portal ScreenCast API实现无闪白视频流
支持全屏或窗口选择模式
窗口模式下通过wmctrl获取准确的窗口位置进行裁剪
"""

import usb.core
import usb.util
import struct
import time
import sys
import argparse
import os
import subprocess
import numpy as np
import queue
import dbus
import dbus.types
from dbus.mainloop.glib import DBusGMainLoop
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib
from PIL import Image

# 初始化
Gst.init(None)
DBusGMainLoop(set_as_default=True)

# USB设备参数
VID = 0x303a
PID = 0x2986

# 屏幕参数
WIDTH = 800
HEIGHT = 480

# 图像类型
UDISP_TYPE_RGB565 = 0
UDISP_TYPE_JPG = 3

# 使用JPEG压缩提高帧率
USE_JPEG = True
JPEG_QUALITY = 70  # 提高质量减少解码计算量 (35太低了会增加解码器负担)

# 旋转模式
ROTATION = 0

# 窗口裁剪区域 (用于窗口模式下裁剪出正确的窗口内容)
CROP_X = 0
CROP_Y = 0
CROP_W = 0
CROP_H = 0

# 全局变量
frame_queue = queue.Queue(maxsize=2)
running = True
ep_out = None


def get_windows():
    """获取窗口列表"""
    windows = []
    try:
        result = subprocess.run(['wmctrl', '-lG'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 8:
                        win_id = parts[0]
                        x = int(parts[2])
                        y = int(parts[3])
                        w = int(parts[4])
                        h = int(parts[5])
                        # 窗口标题从第8个字段开始（可能有空格）
                        title = ' '.join(parts[7:])
                        windows.append({
                            'id': win_id,
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'title': title
                        })
    except Exception as e:
        print(f"获取窗口列表失败: {e}")
    return windows


def select_window_interactive():
    """交互式选择窗口"""
    windows = get_windows()
    if not windows:
        print("未找到窗口列表，请在Portal对话框中选择窗口")
        return None

    print("\n可用窗口:")
    print("-" * 60)
    for i, w in enumerate(windows):
        print(f"  [{i+1}] {w['title']}")
        print(f"      位置: ({w['x']}, {w['y']}) 大小: {w['width']}x{w['height']}")
    print("-" * 60)
    print("  [0] 在Portal对话框中选择（不裁剪）")
    print("  [Q] 退出")

    try:
        choice = input("\n请选择窗口编号: ").strip().upper()
        if choice == 'Q' or choice == '':
            return None
        if choice == '0':
            return None  # 使用Portal默认行为

        idx = int(choice) - 1
        if 0 <= idx < len(windows):
            w = windows[idx]
            print(f"已选择窗口: {w['title']} ({w['width']}x{w['height']})")
            return (w['x'], w['y'], w['width'], w['height'], w['title'])
        else:
            print("无效选择")
            return None
    except ValueError:
        print("无效输入")
        return None
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
    """创建帧头 - 包含同步标记"""
    # 同步标记：4字节特殊序列 "UDSP" (Unique Display Sync Pattern)
    SYNC_MARKER = b'UDSP'

    frame_id_payload = ((frame_id & 0x3FF) | ((payload_size & 0x3FFFFF) << 10))
    header_data = struct.pack('<BBHHHHI',
        frame_type, 0, 0, 0, width, height, frame_id_payload)
    crc = crc16(header_data)
    full_header = struct.pack('<H', crc) + header_data
    # 帧头结构：同步标记(4字节) + CRC+数据(16字节) + 填充(492字节) = 512字节
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
    global ep_out, ROTATION, CROP_X, CROP_Y, CROP_W, CROP_H

    if ep_out is None:
        return False, 0

    if frame_id == 0:
        print(f"捕获图像原始尺寸: {img.size}")
        if CROP_W > 0 and CROP_H > 0:
            print(f"裁剪区域: ({CROP_X}, {CROP_Y}) {CROP_W}x{CROP_H}")

    # 窗口裁剪（在缩放之前）
    if CROP_W > 0 and CROP_H > 0:
        img_w, img_h = img.size
        # 检查裁剪区域是否完全在图像范围内
        if CROP_X + CROP_W <= img_w and CROP_Y + CROP_H <= img_h:
            # 裁剪区域有效，执行裁剪
            img = img.crop((CROP_X, CROP_Y, CROP_X + CROP_W, CROP_Y + CROP_H))
            if frame_id == 0:
                print(f"裁剪后尺寸: {img.size}")
        else:
            # 裁剪区域超出图像范围，说明Portal已返回窗口内容，跳过裁剪
            if frame_id == 0:
                print(f"裁剪区域({CROP_X},{CROP_Y}){CROP_W}x{CROP_H}超出图像范围，跳过裁剪")

    # 旋转图像
    if ROTATION != 0:
        img = img.rotate(-ROTATION, expand=True)
        if frame_id == 0:
            print(f"旋转后尺寸: {img.size} (旋转{ROTATION}度)")

    # 调整大小 - 保持宽高比
    if img.size != (WIDTH, HEIGHT):
        orig_w, orig_h = img.size
        scale = min(WIDTH / orig_w, HEIGHT / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        if frame_id == 0:
            print(f"缩放计算: {orig_w}x{orig_h} -> scale={scale:.3f} -> {new_w}x{new_h}")
        img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

        if img.size != (WIDTH, HEIGHT):
            result = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
            paste_x = (WIDTH - new_w) // 2
            paste_y = (HEIGHT - new_h) // 2
            if frame_id == 0:
                print(f"居中粘贴: offset=({paste_x}, {paste_y})")
            result.paste(img, (paste_x, paste_y))
            img = result

    if USE_JPEG:
        import io
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=JPEG_QUALITY, optimize=True)
        data = buffer.getvalue()
        frame_type = UDISP_TYPE_JPG
    else:
        data = rgb565_convert(img)
        frame_type = UDISP_TYPE_RGB565

    payload_size = len(data)
    header = create_frame_header(WIDTH, HEIGHT, payload_size, frame_type, frame_id)

    try:
        ep_out.write(header)
        # 减小块大小以匹配ESP32接收缓冲区 (4096字节)
        chunk_size = 4096
        for offset in range(0, len(data), chunk_size):
            ep_out.write(data[offset:offset + chunk_size])
        return True, payload_size
    except usb.core.USBError as e:
        print(f"发送失败: {e}")
        return False, 0


class PortalScreenCast:
    def __init__(self):
        self.session_handle = None
        self.pipewire_fd = None
        self.pipewire_node_id = None
        self.pipeline = None
        self.window_size = None
        self.started = False
        self.start_failed = False

    def start(self, select_window=False, callback=None):
        """启动Portal，callback是成功后的回调"""
        self._callback = callback
        self._select_window = select_window
        self._start_portal()

    def _start_portal(self):
        try:
            bus = dbus.SessionBus()
            portal = bus.get_object('org.freedesktop.portal.Desktop', '/org/freedesktop/portal/desktop')
            screencast = dbus.Interface(portal, 'org.freedesktop.portal.ScreenCast')

            import random
            session_token = f'session_{random.randint(10000, 99999)}'
            # 使用 request_token 作为 handle_token，这是关键修复
            request_token1 = f'req1_{random.randint(10000, 99999)}'
            request_token2 = f'req2_{random.randint(10000, 99999)}'
            request_token3 = f'req3_{random.randint(10000, 99999)}'

            print("\n请求屏幕捕获权限...")
            if self._select_window:
                print("请在对话框中选择要投屏的窗口")
            else:
                print("请在对话框中选择要投屏的屏幕")

            # 动态获取sender ID
            sender = bus.get_unique_name()
            sender_id = sender.lstrip(':').replace('.', '_')
            print(f"DBus sender: {sender} -> {sender_id}")

            # 信号路径基于 handle_token (request_token)
            request_path1 = f'/org/freedesktop/portal/desktop/request/{sender_id}/{request_token1}'
            request_path2 = f'/org/freedesktop/portal/desktop/request/{sender_id}/{request_token2}'
            request_path3 = f'/org/freedesktop/portal/desktop/request/{sender_id}/{request_token3}'

            def on_session(code, results):
                if code == 0 and 'session_handle' in results:
                    self.session_handle = str(results['session_handle'])
                    print(f"会话创建成功: {self.session_handle}")
                    # 继续下一步
                    self._select_sources(screencast, request_token2, request_path2, request_token3, request_path3)
                else:
                    print(f"会话创建失败: code={code}")
                    self.start_failed = True

            bus.add_signal_receiver(on_session, 'Response', 'org.freedesktop.portal.Request',
                                    bus_name='org.freedesktop.portal.Desktop',
                                    path=request_path1)

            # 关键修复：添加 handle_token 参数
            screencast.CreateSession({
                'session_handle_token': dbus.String(session_token, variant_level=1),
                'handle_token': dbus.String(request_token1, variant_level=1)
            })

        except Exception as e:
            print(f"启动失败: {e}")
            import traceback
            traceback.print_exc()
            self.start_failed = True

    def _select_sources(self, screencast, request_token, request_path, start_token, start_path):
        bus = dbus.SessionBus()

        source_types = dbus.UInt32(2 if self._select_window else 1, variant_level=1)
        print(f"请求源类型: {source_types} ({'窗口' if self._select_window else '屏幕'})")

        def on_sources(code, results):
            print(f"SelectSources响应: code={code}, results={results}")
            if code == 0:
                print("\n" + "=" * 50)
                if self._select_window:
                    print("【窗口选择模式】请在对话框中选择窗口并点击Share!")
                else:
                    print("【全屏模式】请选择屏幕并点击Share!")
                print("=" * 50)
                self._start_capture(screencast, start_token, start_path)
            else:
                print(f"源选择失败: code={code}")
                self.start_failed = True

        bus.add_signal_receiver(on_sources, 'Response', 'org.freedesktop.portal.Request',
                                bus_name='org.freedesktop.portal.Desktop',
                                path=request_path)

        # 关键修复：添加 handle_token 参数
        options = {
            'handle_token': dbus.String(request_token, variant_level=1),
            'types': source_types,
            'multiple': dbus.Boolean(False, variant_level=1),
            'cursor_mode': dbus.UInt32(1, variant_level=1),
        }
        screencast.SelectSources(dbus.ObjectPath(self.session_handle), options)

    def _start_capture(self, screencast, start_token, start_path):
        bus = dbus.SessionBus()

        def on_start(code, results):
            print(f"Start响应: code={code}, results={results}")
            if code == 0 and 'streams' in results:
                streams = results['streams']
                stream_info = streams[0]
                self.pipewire_node_id = int(stream_info[0])
                if len(stream_info) > 1:
                    props = stream_info[1]
                    if 'size' in props:
                        self.window_size = (int(props['size'][0]), int(props['size'][1]))
                        print(f"捕获尺寸: {self.window_size}")

                print(f"NodeId: {self.pipewire_node_id}")

                fd_reply = screencast.OpenPipeWireRemote(dbus.ObjectPath(self.session_handle), {})
                self.pipewire_fd = fd_reply.take() if isinstance(fd_reply, dbus.types.UnixFd) else int(fd_reply)
                print(f"PipeWire FD: {self.pipewire_fd}")

                if self._start_pipeline():
                    self.started = True
                    if self._callback:
                        self._callback()
                else:
                    self.start_failed = True
            else:
                print(f"启动失败: code={code}")
                self.start_failed = True

        bus.add_signal_receiver(on_start, 'Response', 'org.freedesktop.portal.Request',
                                bus_name='org.freedesktop.portal.Desktop',
                                path=start_path)

        # 使用 dbus.ObjectPath 包装 session_handle
        screencast.Start(dbus.ObjectPath(self.session_handle), '', {'handle_token': dbus.String(start_token, variant_level=1)})

    def _start_pipeline(self):
        # pipewiresrc输出原生格式，videoconvert转换为RGB
        pipeline_str = (
            f"pipewiresrc fd={self.pipewire_fd} path={self.pipewire_node_id} ! "
            f"videoconvert ! "
            f"video/x-raw,format=RGB ! "
            f"appsink name=sink emit-signals=true drop=true max-buffers=2 sync=false"
        )
        print(f"管道: {pipeline_str}")

        try:
            self.pipeline = Gst.parse_launch(pipeline_str)
            sink = self.pipeline.get_by_name('sink')
            sink.connect('new-sample', self._on_frame)

            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._on_message)

            ret = self.pipeline.set_state(Gst.State.PLAYING)
            print(f"管道状态: {ret.value_nick}")
            return ret in (Gst.StateChangeReturn.SUCCESS, Gst.StateChangeReturn.ASYNC)
        except Exception as e:
            print(f"管道启动失败: {e}")
            return False

    def _on_frame(self, sink):
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
                        # 获取stride（每行字节数）
                        if structure.has_field('stride'):
                            stride = structure.get_value('stride')
                        else:
                            stride = frame_w * 3  # 默认RGB 3字节/像素
                    else:
                        frame_w, frame_h, stride = WIDTH, HEIGHT, WIDTH * 3

                    # 使用stride正确提取每一行数据，避免内存对齐导致的撕裂
                    data = np.frombuffer(info.data, dtype=np.uint8)
                    # 按stride提取有效行数据并拼接
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
                                frame_queue.get_nowait()
                            except:
                                pass
                        try:
                            frame_queue.put_nowait(img)
                        except:
                            pass
                except Exception as e:
                    print(f"帧处理错误: {e}")
                    pass
                buf.unmap(info)
        return Gst.FlowReturn.OK

    def _on_message(self, bus, msg):
        if msg.type == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            print(f"GStreamer错误: {err}")

    def stop(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
        if self.pipewire_fd:
            try:
                os.close(self.pipewire_fd)
            except:
                pass


def capture_screenshot():
    """单帧截屏测试"""
    global ep_out, ROTATION, CROP_X, CROP_Y, CROP_W, CROP_H

    ep_out = find_usb_device()
    if not ep_out:
        return

    print("\n=== 单帧截屏测试 ===")
    cast = PortalScreenCast()
    loop = GLib.MainLoop()
    captured = [False]

    def on_started():
        print("已捕获帧，正在处理...")

    def capture_frame_callback():
        """捕获单帧后退出"""
        if captured[0]:
            return False

        try:
            img = frame_queue.get_nowait()
            if img:
                # 发送到ESP32
                ok, size = send_frame(img, 0)
                if ok:
                    print(f"  发送成功: {size} bytes")

                # 保存本地截图
                screenshot_path = '/tmp/screenshot.png'
                img.save(screenshot_path)
                print(f"  本地截图已保存: {screenshot_path}")

                captured[0] = True
                loop.quit()
        except queue.Empty:
            pass
        return True

    cast.start(callback=on_started)
    GLib.timeout_add(100, capture_frame_callback)

    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    cast.stop()
    print("截屏完成")


def main():
    parser = argparse.ArgumentParser(description='ESP32-P4 无闪白屏幕投屏')
    parser.add_argument('-w', '--window', action='store_true', help='窗口选择模式')
    parser.add_argument('--no-test', action='store_true', help='跳过测试颜色')
    parser.add_argument('-r', '--rotate', type=int, default=0, choices=[0, 90, 180, 270],
                        help='旋转角度: 0, 90, 180, 270')
    parser.add_argument('--crop', type=str, default='',
                        help='手动指定裁剪区域: x,y,width,height')
    parser.add_argument('-s', '--screenshot', action='store_true', help='单帧截屏测试')
    args = parser.parse_args()

    if args.screenshot:
        capture_screenshot()
        return

    global ROTATION, ep_out, CROP_X, CROP_Y, CROP_W, CROP_H
    ROTATION = args.rotate

    print("=" * 50)
    print("ESP32-P4 无闪白屏幕投屏 (Portal ScreenCast)")
    if args.rotate != 0:
        print(f"旋转模式: {args.rotate}度")
    print("=" * 50)

    # 裁剪设置（全屏和窗口模式都可用）
    if args.crop:
        try:
            parts = [int(p.strip()) for p in args.crop.split(',')]
            if len(parts) == 4:
                CROP_X, CROP_Y, CROP_W, CROP_H = parts
                print(f"裁剪区域: ({CROP_X}, {CROP_Y}) {CROP_W}x{CROP_H}")
        except:
            print("裁剪区域格式错误: x,y,width,height")
    elif args.window:
        # 窗口模式下交互式选择裁剪区域
        window_info = select_window_interactive()
        if window_info:
            CROP_X, CROP_Y, CROP_W, CROP_H, title = window_info
            print(f"将裁剪窗口区域: ({CROP_X}, {CROP_Y}) {CROP_W}x{CROP_H}")
        else:
            print("未选择窗口，将使用Portal返回的完整图像")

    ep_out = find_usb_device()
    if not ep_out:
        return

    if not args.no_test:
        print("\n发送测试颜色...")
        # 临时清除裁剪参数，因为测试色图像尺寸小于裁剪区域
        saved_crop = (CROP_X, CROP_Y, CROP_W, CROP_H)
        CROP_X, CROP_Y, CROP_W, CROP_H = 0, 0, 0, 0
        for i, (name, r, g, b) in enumerate([("红",255,0,0), ("绿",0,255,0), ("蓝",0,0,255)]):
            img = Image.new('RGB', (WIDTH, HEIGHT), (r, g, b))
            # 测试色也需要旋转
            if ROTATION != 0:
                img = img.rotate(-ROTATION, expand=True)
                # 旋转后重新缩放到屏幕尺寸
                img = img.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
            if send_frame(img, i)[0]:
                print(f"  {name}: OK")
            time.sleep(0.3)
        CROP_X, CROP_Y, CROP_W, CROP_H = saved_crop

    cast = PortalScreenCast()

    loop = GLib.MainLoop()

    # 帧发送状态
    frame_id = 0
    total = 0
    last = time.time()
    count = 0

    def on_portal_started():
        """Portal启动成功后的回调"""
        print("\n开始投屏... (Ctrl+C停止)")
        print("-" * 50)
        if args.window:
            print("【窗口模式】")
            if CROP_W > 0 and CROP_H > 0:
                print(f"裁剪区域: ({CROP_X}, {CROP_Y}) {CROP_W}x{CROP_H}")
            if cast.window_size:
                print(f"Portal返回尺寸: {cast.window_size}")
        else:
            print("【全屏模式】")

        # 启动帧发送定时器 - 降低帧率给ESP32更多处理时间
        # ESP32 JPEG解码800x480约需50-100ms，降低帧率避免缓冲耗尽
        GLib.timeout_add(100, send_frame_callback)  # ~10fps (测试用)

    def send_frame_callback():
        """定时发送帧"""
        nonlocal frame_id, total, last, count

        try:
            img = frame_queue.get_nowait()
            ok, size = send_frame(img, frame_id)
            if ok:
                total += size
                count += 1
                frame_id += 1

            now = time.time()
            if now - last >= 1.0:
                fps = count / (now - last)
                bitrate = total * 8 / (now - last) / 1000
                print(f"FPS: {fps:.1f} | 带宽: {bitrate:.0f}kbps | 帧: {frame_id}")
                last = now
                count = 0
                total = 0
        except queue.Empty:
            pass

        return True  # 继续运行

    def check_failed():
        """检查是否启动失败"""
        if cast.start_failed:
            print("Portal启动失败")
            loop.quit()
            return False
        return True

    # 启动Portal
    cast.start(select_window=args.window, callback=on_portal_started)

    # 定时检查失败状态
    GLib.timeout_add(500, check_failed)

    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    print(f"\n停止 - 总帧数: {frame_id}")
    cast.stop()


if __name__ == '__main__':
    main()