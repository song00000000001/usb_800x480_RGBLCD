#!/usr/bin/env python3
"""
ESP32-P4 USB 屏幕投屏脚本 - Mutter ScreenCast版本
直接使用 Mutter ScreenCast API + PipeWire 实现视频流捕获
支持显示器选择、窗口录制、区域录制
适用于 GNOME Shell 46+ (绕过 Portal bug)
"""

import usb.core
import usb.util
import struct
import time
import sys
import argparse
import os
import subprocess
import tempfile
import numpy as np
import queue
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib
from PIL import Image

# 初始化
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

# 使用JPEG压缩
USE_JPEG = True
JPEG_QUALITY = 35

# 旋转和偏移
ROTATION = 0
OFFSET_X = 0
OFFSET_Y = 0

# 全局变量
ep_out = None
frame_queue = queue.Queue(maxsize=2)


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
    frame_id_payload = ((frame_id & 0x3FF) | ((payload_size & 0x3FFFFF) << 10))
    header_data = struct.pack('<BBHHHHI',
        frame_type, 0, 0, 0, width, height, frame_id_payload)
    crc = crc16(header_data)
    full_header = struct.pack('<H', crc) + header_data
    return full_header + bytes(512 - len(full_header))


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
    global ep_out, ROTATION, OFFSET_X, OFFSET_Y

    if ep_out is None:
        return False, 0

    # 旋转图像
    if ROTATION != 0:
        img = img.rotate(-ROTATION, expand=True)

    # 调整大小 - 保持宽高比
    if img.size != (WIDTH, HEIGHT):
        orig_w, orig_h = img.size
        scale = min(WIDTH / orig_w, HEIGHT / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

        if img.size != (WIDTH, HEIGHT):
            result = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
            paste_x = (WIDTH - new_w) // 2 + OFFSET_X
            paste_y = (HEIGHT - new_h) // 2 + OFFSET_Y
            paste_x = max(0, min(paste_x, WIDTH - new_w))
            paste_y = max(0, min(paste_y, HEIGHT - new_h))
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
        chunk_size = 49152
        for offset in range(0, len(data), chunk_size):
            ep_out.write(data[offset:offset + chunk_size])
        return True, payload_size
    except usb.core.USBError as e:
        print(f"发送失败: {e}")
        return False, 0


class MutterScreenCast:
    """直接使用 Mutter ScreenCast API"""

    def __init__(self):
        self.bus = dbus.SessionBus()
        self.session_path = None
        self.stream_path = None
        self.node_id = None
        self.pipeline = None
        self.started = False

    def get_windows(self):
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

    def select_window_interactive(self):
        """交互式选择窗口"""
        windows = self.get_windows()
        if not windows:
            print("未找到窗口，使用 gnome-screenshot 选择...")
            return self._select_window_by_click()

        print("\n可用窗口:")
        print("-" * 60)
        for i, w in enumerate(windows):
            print(f"  [{i+1}] {w['title']}")
            print(f"      位置: ({w['x']}, {w['y']}) 大小: {w['width']}x{w['height']}")
        print("-" * 60)
        print("  [0] 点击选择窗口")
        print("  [Q] 退出")

        try:
            choice = input("\n请选择窗口编号: ").strip().upper()
            if choice == 'Q' or choice == '':
                return None
            if choice == '0':
                return self._select_window_by_click()

            idx = int(choice) - 1
            if 0 <= idx < len(windows):
                w = windows[idx]
                return (w['x'], w['y'], w['width'], w['height'], w['title'])
            else:
                print("无效选择")
                return None
        except ValueError:
            print("无效输入")
            return None

    def _select_window_by_click(self):
        """通过点击选择窗口"""
        print("\n请点击要投屏的窗口...")
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name

            result = subprocess.run(
                ['gnome-screenshot', '-w', '-B', '-f', tmp_path],
                capture_output=True,
                timeout=60
            )

            if result.returncode == 0 and os.path.exists(tmp_path):
                # 获取窗口信息需要通过其他方式
                # gnome-screenshot -w 截取的是窗口内容，我们需要找到窗口位置
                img = Image.open(tmp_path)
                os.unlink(tmp_path)

                # 尝试从 wmctrl 匹配窗口大小
                windows = self.get_windows()
                for w in windows:
                    if w['width'] == img.width and w['height'] == img.height:
                        print(f"选中窗口: {w['title']}")
                        return (w['x'], w['y'], w['width'], w['height'], w['title'])

                # 如果没有精确匹配，返回截图尺寸，位置需要用户确认
                print(f"窗口大小: {img.width}x{img.height}")
                print("提示: 使用 --area 参数手动指定位置")
                return (0, 0, img.width, img.height, "未知窗口")

            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except subprocess.TimeoutExpired:
            print("窗口选择超时")
        except Exception as e:
            print(f"窗口选择失败: {e}")

        return None

    def get_monitors(self):
        """获取显示器列表"""
        try:
            display_config = self.bus.get_object(
                'org.gnome.Mutter.DisplayConfig',
                '/org/gnome/Mutter/DisplayConfig'
            )
            iface = dbus.Interface(display_config, 'org.gnome.Mutter.DisplayConfig')
            serial, monitors, logical_monitors, properties = iface.GetCurrentState()

            monitor_list = []
            for m in monitors:
                if len(m) >= 2:
                    monitor_info = m[0]
                    if len(monitor_info) >= 4:
                        connector = str(monitor_info[0])
                        vendor = str(monitor_info[1])
                        product = str(monitor_info[2])

                        # 获取当前模式信息
                        modes = m[1]
                        current_mode = None
                        for mode in modes:
                            if len(mode) >= 7:
                                mode_props = mode[6] if len(mode) > 6 else {}
                                if mode_props.get('is-current', False):
                                    current_mode = {
                                        'name': str(mode[0]),
                                        'width': int(mode[1]),
                                        'height': int(mode[2]),
                                        'refresh': float(mode[3])
                                    }
                                    break

                        monitor_list.append({
                            'connector': connector,
                            'vendor': vendor,
                            'product': product,
                            'mode': current_mode
                        })
            return monitor_list
        except Exception as e:
            print(f"获取显示器列表失败: {e}")
            return []

    def start_monitor(self, connector=''):
        """录制指定显示器"""
        print(f"\n录制显示器: {connector if connector else '默认'}")
        return self._start_stream('monitor', connector)

    def start_window_by_id(self, window_id):
        """通过窗口ID录制指定窗口"""
        print(f"\n录制窗口ID: {window_id}")
        return self._start_stream('window', None, window_id=window_id)

    def start_area(self, x, y, width, height):
        """录制指定区域"""
        print(f"\n录制区域: ({x}, {y}) {width}x{height}")
        return self._start_stream('area', (x, y, width, height))

    def _start_stream(self, stream_type, param, window_id=None):
        """启动视频流"""
        try:
            mutter = self.bus.get_object(
                'org.gnome.Mutter.ScreenCast',
                '/org/gnome/Mutter/ScreenCast'
            )
            screencast = dbus.Interface(mutter, 'org.gnome.Mutter.ScreenCast')

            self.session_path = screencast.CreateSession(
                dbus.Dictionary({}, signature='sv')
            )
            print(f"Session: {self.session_path}")

            session = self.bus.get_object('org.gnome.Mutter.ScreenCast', self.session_path)
            session_iface = dbus.Interface(session, 'org.gnome.Mutter.ScreenCast.Session')

            options = dbus.Dictionary({}, signature='sv')

            if stream_type == 'monitor':
                self.stream_path = session_iface.RecordMonitor(param or '', options)
            elif stream_type == 'window':
                if window_id:
                    options['window-id'] = dbus.UInt32(int(window_id, 16))
                self.stream_path = session_iface.RecordWindow(options)
            elif stream_type == 'area':
                x, y, w, h = param
                self.stream_path = session_iface.RecordArea(x, y, w, h, options)

            print(f"Stream: {self.stream_path}")

            # 获取 Stream 参数
            props = dbus.Interface(
                self.bus.get_object('org.gnome.Mutter.ScreenCast', self.stream_path),
                'org.freedesktop.DBus.Properties'
            )
            params = props.GetAll('org.gnome.Mutter.ScreenCast.Stream')
            print(f"Stream Parameters: {params.get('Parameters', {})}")

            # 使用 GLib MainLoop 等待信号
            wait_loop = GLib.MainLoop()
            start_result = [False]  # 使用列表存储结果（闭包可修改）

            def on_pipewire_stream_added(node_id):
                self.node_id = int(node_id)
                print(f"PipeWire node_id: {self.node_id}")
                if self._start_pipeline():
                    self.started = True
                    start_result[0] = True
                wait_loop.quit()

            def on_timeout():
                print("等待 PipeWire 信号超时")
                wait_loop.quit()
                return False

            self.bus.add_signal_receiver(
                on_pipewire_stream_added,
                'PipeWireStreamAdded',
                'org.gnome.Mutter.ScreenCast.Stream',
                bus_name='org.gnome.Mutter.ScreenCast',
                path=self.stream_path
            )

            # 启动 Session
            print("启动 Session...")
            session_iface.Start()

            # 使用 GLib 超时等待信号
            GLib.timeout_add_seconds(5, on_timeout)
            wait_loop.run()

            return start_result[0]

        except Exception as e:
            print(f"启动失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _start_pipeline(self):
        """启动 GStreamer PipeWire 管道"""
        if self.node_id is None:
            return False

        pipeline_str = (
            f"pipewiresrc path={self.node_id} ! "
            f"videoconvert ! "
            f"appsink name=sink emit-signals=true drop=true max-buffers=2 sync=false"
        )
        print(f"GStreamer Pipeline: {pipeline_str}")

        try:
            self.pipeline = Gst.parse_launch(pipeline_str)
            sink = self.pipeline.get_by_name('sink')
            sink.connect('new-sample', self._on_frame)

            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self._on_message)

            ret = self.pipeline.set_state(Gst.State.PLAYING)
            print(f"Pipeline 状态: {ret.value_nick}")
            return ret in (Gst.StateChangeReturn.SUCCESS, Gst.StateChangeReturn.ASYNC)
        except Exception as e:
            print(f"Pipeline 启动失败: {e}")
            return False

    def _on_frame(self, sink):
        """处理视频帧"""
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
                    else:
                        frame_w, frame_h = WIDTH, HEIGHT

                    data = np.frombuffer(info.data, dtype=np.uint8)[:frame_w * frame_h * 3]
                    if len(data) == frame_w * frame_h * 3:
                        img = Image.frombuffer('RGB', (frame_w, frame_h), data, 'raw', 'RGB', 0, 1)

                        if frame_queue.full():
                            try:
                                frame_queue.get_nowait()
                            except:
                                pass
                        try:
                            frame_queue.put_nowait(img)
                        except:
                                pass
                except:
                    pass
                buf.unmap(info)
        return Gst.FlowReturn.OK

    def _on_message(self, bus, msg):
        """处理 GStreamer 消息"""
        if msg.type == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            print(f"GStreamer 错误: {err}")

    def stop(self):
        """停止捕获"""
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
        self.started = False


def main():
    # 初始化 DBus MainLoop
    DBusGMainLoop(set_as_default=True)

    parser = argparse.ArgumentParser(
        description='ESP32-P4 屏幕投屏 (Mutter ScreenCast API)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 录制默认显示器
  %(prog)s -m DP-1            # 录制指定显示器
  %(prog)s -w                 # 交互式选择窗口录制
  %(prog)s -i 0x3800004       # 录制指定窗口ID
  %(prog)s -W                 # 显示窗口列表
  %(prog)s -a 100,100,800,600 # 录制指定区域
  %(prog)s --list             # 显示显示器列表
        """
    )
    parser.add_argument('-m', '--monitor', type=str, default='',
                        help='指定显示器 connector (如 DP-1)')
    parser.add_argument('-w', '--window', action='store_true',
                        help='录制窗口模式（交互选择）')
    parser.add_argument('-W', '--window-list', action='store_true',
                        help='显示窗口列表')
    parser.add_argument('-i', '--window-id', type=str,
                        help='指定窗口ID (十六进制, 如 0x3800004)')
    parser.add_argument('-a', '--area', type=str,
                        help='录制区域 x,y,width,height')
    parser.add_argument('--list', action='store_true',
                        help='显示显示器列表')
    parser.add_argument('--no-test', action='store_true',
                        help='跳过测试颜色')
    parser.add_argument('-r', '--rotate', type=int, default=0,
                        choices=[0, 90, 180, 270], help='旋转角度')
    parser.add_argument('--offset', type=str, default='0,0',
                        help='偏移 x,y (调整图像居中位置)')
    parser.add_argument('--quality', type=int, default=35,
                        help='JPEG质量 (1-100)')
    args = parser.parse_args()

    global ROTATION, OFFSET_X, OFFSET_Y, USE_JPEG, JPEG_QUALITY
    ROTATION = args.rotate
    JPEG_QUALITY = args.quality

    try:
        offset_parts = [int(p.strip()) for p in args.offset.split(',')]
        if len(offset_parts) >= 2:
            OFFSET_X, OFFSET_Y = offset_parts[0], offset_parts[1]
    except:
        pass

    print("=" * 50)
    print("ESP32-P4 屏幕投屏 (Mutter ScreenCast API)")
    print("=" * 50)

    # 显示器列表
    if args.list:
        cast = MutterScreenCast()
        monitors = cast.get_monitors()
        print("\n可用显示器:")
        for m in monitors:
            mode_info = ""
            if m['mode']:
                mode_info = f" {m['mode']['width']}x{m['mode']['height']} @ {m['mode']['refresh']:.0f}Hz"
            print(f"  {m['connector']}: {m['vendor']} {m['product']}{mode_info}")
        return

    # 窗口列表
    if args.window_list:
        cast = MutterScreenCast()
        windows = cast.get_windows()
        if windows:
            print("\n可用窗口:")
            print("-" * 60)
            for i, w in enumerate(windows):
                print(f"  [{i+1}] {w['title']}")
                print(f"      位置: ({w['x']}, {w['y']}) 大小: {w['width']}x{w['height']}")
        else:
            print("未找到窗口")
        return

    # 查找 USB 设备
    global ep_out
    ep_out = find_usb_device()
    if not ep_out:
        return

    # 测试颜色
    if not args.no_test:
        print("\n发送测试颜色...")
        for name, r, g, b in [("红", 255, 0, 0), ("绿", 0, 255, 0),
                             ("蓝", 0, 0, 255), ("白", 255, 255, 255)]:
            img = Image.new('RGB', (WIDTH, HEIGHT), (r, g, b))
            if send_frame(img, 0)[0]:
                print(f"  {name}: OK")
            time.sleep(0.3)

    # 创建 ScreenCast
    cast = MutterScreenCast()

    # 选择录制模式
    if args.window_id:
        if not cast.start_window_by_id(args.window_id):
            print("窗口录制启动失败")
            return
    elif args.window:
        selected = cast.select_window_interactive()
        if selected is None:
            print("未选择窗口")
            return
        x, y, w, h, title = selected
        print(f"将录制窗口: {title}")
        print(f"区域: ({x}, {y}) {w}x{h}")
        if not cast.start_area(x, y, w, h):
            print("窗口录制启动失败")
            return
    elif args.area:
        try:
            parts = [int(p.strip()) for p in args.area.split(',')]
            if len(parts) == 4:
                if not cast.start_area(parts[0], parts[1], parts[2], parts[3]):
                    print("区域录制启动失败")
                    return
            else:
                print("区域格式错误: x,y,width,height")
                return
        except:
            print("区域格式错误")
            return
    else:
        if not cast.start_monitor(args.monitor):
            print("显示器录制启动失败")
            return

    if not cast.started:
        print("视频流启动失败")
        return

    print("\n开始投屏... (Ctrl+C 停止)")
    print("-" * 50)

    # 帧发送循环
    loop = GLib.MainLoop()
    frame_id = 0
    total_bytes = 0
    last_time = time.time()
    fps_count = 0

    def send_frame_callback():
        global frame_id, total_bytes, last_time, fps_count
        try:
            img = frame_queue.get_nowait()
            ok, size = send_frame(img, frame_id)
            if ok:
                total_bytes += size
                fps_count += 1
                frame_id += 1

            now = time.time()
            if now - last_time >= 1.0:
                fps = fps_count / (now - last_time)
                bitrate = total_bytes * 8 / (now - last_time) / 1000
                print(f"FPS: {fps:.1f} | 带宽: {bitrate:.0f}kbps | 帧: {frame_id}")
                last_time = now
                fps_count = 0
                total_bytes = 0
        except queue.Empty:
            pass
        return True

    GLib.timeout_add(16, send_frame_callback)  # ~60fps

    try:
        loop.run()
    except KeyboardInterrupt:
        pass

    print(f"\n停止 - 总帧数: {frame_id}")
    cast.stop()


if __name__ == '__main__':
    main()