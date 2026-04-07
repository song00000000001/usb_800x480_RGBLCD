#!/usr/bin/env python3
"""
ESP32-P4 极限帧率压力测试
逐步提高发送帧率，测量USB接收帧率和LCD显示帧率
"""

import usb.core
import usb.util
import struct
import time
import argparse
import numpy as np
from PIL import Image
import io

# USB设备参数
VID = 0x303A
PID = 0x2986

# 屏幕参数
WIDTH = 800
HEIGHT = 480

# 图像类型
UDISP_TYPE_RGB565 = 0
UDISP_TYPE_JPG = 3

# 测试参数
TEST_DURATION_SEC = 3.0  # 每个帧率测试持续时间
FRAME_RATES_TO_TEST = [5, 10, 15, 20, 24, 30, 45, 60, 90, 120]


def crc16(data):
    """计算CRC16校验 (Modbus)"""
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
    """创建帧头 - 填充到512字节"""
    SYNC_MARKER = b'UDSP'
    # frame_id (10bit) + payload_total (22bit)
    frame_id_payload = ((frame_id & 0x3FF) | ((payload_size & 0x3FFFFF) << 10))

    header_data = struct.pack('<BBHHHHI',
        frame_type,    # type
        0,             # cmd
        0,             # x
        0,             # y
        width,         # width
        height,        # height
        frame_id_payload
    )
    crc = crc16(header_data)
    full_header = SYNC_MARKER + struct.pack('<H', crc) + header_data
    # 填充到512字节
    return full_header + b'\x00' * (512 - len(full_header))


def create_rgb565_test_pattern(width, height, frame_id):
    """创建彩色测试图案 (RGB565)"""
    pattern = np.zeros((height, width, 3), dtype=np.uint8)
    phase = (frame_id % 4)

    # 4种基本颜色分区
    h_half = height // 2
    w_half = width // 2

    if phase == 0:  # 红色/蓝色棋盘
        for y in range(height):
            for x in range(width):
                if (y // 40 + x // 40) % 2 == 0:
                    pattern[y, x] = [255, 0, 0]
                else:
                    pattern[y, x] = [0, 0, 255]
    elif phase == 1:  # 绿色渐变
        for y in range(height):
            val = int(255 * y / height)
            pattern[y, :] = [0, val, 0]
    elif phase == 2:  # 蓝红渐变
        for x in range(width):
            r = int(255 * x / width)
            b = int(255 * (width - x) / width)
            pattern[:, x] = [r, 0, b]
    else:  # 白色/黑色条纹
        for y in range(height):
            if (y // 10) % 2 == 0:
                pattern[y, :] = [255, 255, 255]
            else:
                pattern[y, :] = [0, 0, 0]

    # 转换RGB565
    r5 = (pattern[:,:,0] >> 3).astype(np.uint16)
    g6 = (pattern[:,:,1] >> 2).astype(np.uint16)
    b5 = (pattern[:,:,2] >> 3).astype(np.uint16)
    rgb565 = (r5 << 11) | (g6 << 5) | b5
    return rgb565.astype('<u2').tobytes()


def create_jpeg_test_frame(width, height, frame_id, quality=30):
    """创建JPEG测试帧"""
    # 创建彩色图案
    pattern = np.zeros((height, width, 3), dtype=np.uint8)
    phase = (frame_id % 8)

    if phase < 4:
        # 渐变背景
        for y in range(height):
            for x in range(width):
                r = int(127 + 127 * np.sin(2 * np.pi * x / width * 2))
                g = int(127 + 127 * np.sin(2 * np.pi * y / height * 2))
                b = int(127 + 127 * np.sin(2 * np.pi * (x + y) / (width + height)))
                pattern[y, x] = [r, g, b]
    else:
        # 彩色条纹
        stripe_w = width // 8
        colors = [[255,0,0], [0,255,0], [0,0,255], [255,255,0],
                  [255,0,255], [0,255,255], [255,255,255], [0,0,0]]
        for i, c in enumerate(colors):
            pattern[:, i*stripe_w:(i+1)*stripe_w] = c

    img = Image.fromarray(pattern, 'RGB')

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=False)
    return buffer.getvalue()


def find_usb_device():
    """查找并配置USB设备"""
    print(f"查找设备 VID=0x{VID:04X}, PID=0x{PID:04X}")
    dev = usb.core.find(idVendor=VID, idProduct=PID)
    if dev is None:
        print("未找到设备!")
        return None

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

    print(f"OUT端点: 0x{ep_out.bEndpointAddress:02X}")
    return ep_out


def send_frame_rgb565(ep_out, frame_id, width=WIDTH, height=HEIGHT):
    """发送一帧RGB565图像"""
    data = create_rgb565_test_pattern(width, height, frame_id)
    header = create_frame_header(width, height, len(data), UDISP_TYPE_RGB565, frame_id)

    try:
        ep_out.write(header)
        chunk_size = 4096
        for offset in range(0, len(data), chunk_size):
            ep_out.write(data[offset:offset + chunk_size])
        return True, len(data)
    except usb.core.USBError as e:
        print(f"发送失败: {e}")
        return False, 0


def send_frame_jpeg(ep_out, frame_id, width=WIDTH, height=HEIGHT, quality=30):
    """发送一帧JPEG图像"""
    data = create_jpeg_test_frame(width, height, frame_id, quality)
    header = create_frame_header(width, height, len(data), UDISP_TYPE_JPG, frame_id)

    try:
        ep_out.write(header)
        chunk_size = 4096
        for offset in range(0, len(data), chunk_size):
            ep_out.write(data[offset:offset + chunk_size])
        return True, len(data)
    except usb.core.USBError as e:
        print(f"发送失败: {e}")
        return False, 0


def run_fps_test(ep_out, target_fps, test_type, duration=TEST_DURATION_SEC):
    """
    运行指定帧率的测试
    test_type: 'rgb565' 或 'jpeg'
    """
    interval = 1.0 / target_fps
    frame_id = 0
    frames_sent = 0
    bytes_sent = 0
    errors = 0

    start_time = time.time()
    last_send_time = start_time

    print(f"\n  目标帧率: {target_fps} fps (间隔: {interval*1000:.1f} ms)")

    while time.time() - start_time < duration:
        now = time.time()
        elapsed = now - last_send_time

        if elapsed >= interval:
            # 发送帧
            if test_type == 'rgb565':
                ok, size = send_frame_rgb565(ep_out, frame_id)
            else:
                ok, size = send_frame_jpeg(ep_out, frame_id)

            if ok:
                frames_sent += 1
                bytes_sent += size
                frame_id += 1
            else:
                errors += 1

            last_send_time = now

        # 避免CPU占用过高
        time.sleep(0.0001)

    actual_fps = frames_sent / duration
    bandwidth_mbps = (bytes_sent * 8) / duration / 1_000_000

    return {
        'target_fps': target_fps,
        'actual_fps': actual_fps,
        'frames_sent': frames_sent,
        'bytes_sent': bytes_sent,
        'bandwidth_mbps': bandwidth_mbps,
        'errors': errors
    }


def run_stress_test(ep_out, test_type='jpeg', duration=TEST_DURATION_SEC):
    """运行压力测试 - 从低帧率逐步提高到高帧率"""
    print("=" * 60)
    print(f"ESP32-P4 极限帧率压力测试")
    print(f"测试类型: {test_type.upper()}")
    print(f"分辨率: {WIDTH}x{HEIGHT}")
    print(f"每种帧率测试时长: {TEST_DURATION_SEC} 秒")
    print("=" * 60)

    results = []

    for fps in FRAME_RATES_TO_TEST:
        print(f"\n>>> 测试 {fps} fps <<<")
        result = run_fps_test(ep_out, fps, test_type, duration)

        print(f"    实际发送: {result['actual_fps']:.1f} fps")
        print(f"    发送带宽: {result['bandwidth_mbps']:.1f} Mbps")
        print(f"    发送帧数: {result['frames_sent']}")
        print(f"    错误数:   {result['errors']}")

        results.append(result)

        # 检查是否出现错误（丢帧）
        if result['errors'] > result['frames_sent'] * 0.1:
            print(f"    [警告] 错误率较高，可能接近极限")

    # 汇总
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"{'目标fps':>8} {'实际fps':>8} {'带宽(Mbps)':>12} {'发送帧数':>8} {'错误数':>8}")
    print("-" * 60)

    for r in results:
        print(f"{r['target_fps']:>8} {r['actual_fps']:>8.1f} {r['bandwidth_mbps']:>12.1f} {r['frames_sent']:>8} {r['errors']:>8}")

    # 分析瓶颈
    print("\n" + "=" * 60)
    print("瓶颈分析")
    print("=" * 60)

    last_actual = 0
    for r in results:
        if r['actual_fps'] < r['target_fps'] * 0.95:
            print(f"  帧率 {r['target_fps']} fps: 未能达到目标，出现瓶颈")
            break
        last_actual = r['actual_fps']

    max_achieved = max(results, key=lambda x: x['actual_fps'])['actual_fps']
    print(f"  最高可达帧率: {max_achieved:.1f} fps")
    print(f"\n  提示: 观察ESP32串口日志中的 'Input fps' 和 'Display fps'")
    print(f"        Input fps > Display fps 表示显示端瓶颈")
    print(f"        Input fps ≈ Display fps 表示USB传输瓶颈")

    return results


def run_single_fps_test(ep_out, fps, test_type='jpeg', duration=5.0):
    """单次帧率测试 - 持续运行供观察"""
    print(f"连续测试 {fps} fps，按 Ctrl+C 停止...")
    print(f"观察ESP32日志中的 Input fps 和 Display fps")
    print()

    frame_id = 0
    interval = 1.0 / fps
    last_send_time = time.time()
    start_time = time.time()
    frames_sent = 0
    bytes_sent = 0

    try:
        while True:
            now = time.time()
            elapsed = now - last_send_time

            if elapsed >= interval:
                if test_type == 'rgb565':
                    ok, size = send_frame_rgb565(ep_out, frame_id)
                else:
                    ok, size = send_frame_jpeg(ep_out, frame_id)

                if ok:
                    frames_sent += 1
                    bytes_sent += size
                    frame_id += 1

                last_send_time = now

            # 每秒打印一次状态
            if now - start_time >= 1.0:
                actual_fps = frames_sent / (now - start_time)
                bw = bytes_sent * 8 / (now - start_time) / 1_000_000
                print(f"\rFPS: {actual_fps:.1f} | 带宽: {bw:.1f} Mbps | 帧: {frame_id}    ", end='', flush=True)
                frames_sent = 0
                bytes_sent = 0
                start_time = now

            time.sleep(0.0001)

    except KeyboardInterrupt:
        print(f"\n测试结束，总发送 {frame_id} 帧")


def main():
    parser = argparse.ArgumentParser(description='ESP32-P4 极限帧率测试')
    parser.add_argument('--fps', type=int, default=0,
                        help='单次测试指定帧率 (0=压力测试模式)')
    parser.add_argument('--type', choices=['rgb565', 'jpeg'], default='jpeg',
                        help='测试类型: rgb565(无解码) 或 jpeg(有解码)')
    parser.add_argument('--duration', type=float, default=TEST_DURATION_SEC,
                        help=f'每种帧率测试持续时间(秒), 默认{TEST_DURATION_SEC}')
    args = parser.parse_args()

    ep_out = find_usb_device()
    if not ep_out:
        return

    if args.fps > 0:
        run_single_fps_test(ep_out, args.fps, args.type, duration=999999)
    else:
        run_stress_test(ep_out, args.type, args.duration)


if __name__ == '__main__':
    main()
