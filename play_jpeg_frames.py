#!/usr/bin/env python3
"""
ESP32-P4 JPEG帧序列播放器
播放 jpeg_frames 目录中的所有帧，24fps
"""

import usb.core
import usb.util
import struct
import time
import os
import glob
import io
import numpy as np
from PIL import Image
import argparse

# USB设备参数
VID = 0x303A
PID = 0x2986

# 屏幕参数
WIDTH = 800
HEIGHT = 480

# 图像类型
UDISP_TYPE_JPG = 3

# 目标帧率
TARGET_FPS = 24

# JPEG压缩质量
JPEG_QUALITY = 85


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
    frame_id_payload = ((frame_id & 0x3FF) | ((payload_size & 0x3FFFFF) << 10))

    header_data = struct.pack('<BBHHHHI',
        frame_type, 0, 0, 0, width, height, frame_id_payload)
    crc = crc16(header_data)
    full_header = SYNC_MARKER + struct.pack('<H', crc) + header_data
    return full_header + b'\x00' * (512 - len(full_header))


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


def reset_usb_device():
    """断开并重置USB设备，让ESP32重新枚举"""
    dev = usb.core.find(idVendor=VID, idProduct=PID)
    if dev:
        try:
            usb.util.release_interface(dev, 0)
        except Exception:
            pass
        try:
            dev.reset()
        except Exception:
            pass
    time.sleep(0.5)


def send_frame(ep_out, jpeg_data, frame_id, width=WIDTH, height=HEIGHT):
    """发送一帧JPEG图像"""
    header = create_frame_header(width, height, len(jpeg_data), UDISP_TYPE_JPG, frame_id)

    try:
        ep_out.write(header)
        chunk_size = 4096
        for offset in range(0, len(jpeg_data), chunk_size):
            ep_out.write(jpeg_data[offset:offset + chunk_size])
        return True
    except usb.core.USBError as e:
        print(f"发送失败: {e}")
        return False


def resize_frame(img):
    """将图片缩放到800x480，保持宽高比，居中放置"""
    orig_w, orig_h = img.size

    # 按比例缩放，适应800x480窗口
    scale = min(WIDTH / orig_w, HEIGHT / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)

    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 创建800x480黑底，将缩放后图片居中
    result = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    paste_x = (WIDTH - new_w) // 2
    paste_y = (HEIGHT - new_h) // 2
    result.paste(img, (paste_x, paste_y))
    return result


def load_jpeg_frames(frames_dir):
    """加载并缩放所有JPEG帧"""
    pattern = os.path.join(frames_dir, "output_*.jpg")
    files = sorted(glob.glob(pattern))

    frames = []
    for f in files:
        img = Image.open(f)
        img_resized = resize_frame(img)
        buf = io.BytesIO()
        img_resized.save(buf, format='JPEG', quality=JPEG_QUALITY, optimize=False)
        frames.append(buf.getvalue())

    total_original = sum(os.path.getsize(f) for f in files)
    total_resized = sum(len(f) for f in frames)
    print(f"加载了 {len(frames)} 帧")
    print(f"  原始: {total_original / 1024 / 1024:.1f} MB -> 缩放后: {total_resized / 1024:.1f} KB")
    return frames


def play(ep_out, frames, target_fps):
    """播放所有帧"""
    interval = 1.0 / target_fps
    total = len(frames)
    sent = 0
    errors = 0
    total_bytes = 0
    start_time = time.time()
    last_print_sec = 0

    print(f"\n开始播放 {total} 帧 @ {target_fps} fps...")

    for i, frame_data in enumerate(frames):
        loop_start = time.time()

        ok = send_frame(ep_out, frame_data, i)
        if ok:
            sent += 1
            total_bytes += len(frame_data)
        else:
            errors += 1

        # 帧间隔控制
        elapsed = time.time() - loop_start
        sleep_time = interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

        # 每秒打印进度
        now = time.time()
        sec = int(now - start_time)
        if sec > last_print_sec:
            actual_fps = sent / (now - start_time) if (now - start_time) > 0 else 0
            bw = total_bytes * 8 / (now - start_time) / 1_000_000 if (now - start_time) > 0 else 0
            progress = (i + 1) / total * 100
            print(f"\r  [{i+1}/{total}] {progress:.1f}% | FPS: {actual_fps:.1f} | 带宽: {bw:.1f} Mbps | 错误: {errors}    ", end='', flush=True)
            last_print_sec = sec

    elapsed = time.time() - start_time
    actual_fps = sent / elapsed if elapsed > 0 else 0
    bw = total_bytes * 8 / elapsed / 1_000_000 if elapsed > 0 else 0

    print(f"\n\n播放完成!")
    print(f"  总帧数: {sent}")
    print(f"  总时间: {elapsed:.2f}秒")
    print(f"  平均帧率: {actual_fps:.1f} fps")
    print(f"  平均带宽: {bw:.1f} Mbps")
    print(f"  错误数: {errors}")

    return sent, errors


def main():
    parser = argparse.ArgumentParser(description='ESP32-P4 JPEG帧序列播放器')
    parser.add_argument('--loop', action='store_true', help='循环播放')
    args = parser.parse_args()

    frames_dir = os.path.join(os.path.dirname(__file__), "jpeg_frames")
    if not os.path.exists(frames_dir):
        print(f"未找到帧目录: {frames_dir}")
        return

    frames = load_jpeg_frames(frames_dir)
    if not frames:
        print("没有加载到帧!")
        return

    print(f"目标帧率: {TARGET_FPS} fps")
    print("-" * 50)

    play_count = 0
    while True:
        ep_out = find_usb_device()
        if not ep_out:
            return

        play_count += 1
        if play_count > 1:
            print(f"\n=== 第 {play_count} 轮播放 ===")

        sent, errors = play(ep_out, frames, TARGET_FPS)

        if not args.loop:
            break

        # 播放完毕，释放USB并重置ESP32，等待后重新连接
        print("\n等待ESP32缓冲清空...")
        time.sleep(2)
        print("重置USB连接...")
        reset_usb_device()
        time.sleep(1)
        print("重新连接设备...")


if __name__ == '__main__':
    main()