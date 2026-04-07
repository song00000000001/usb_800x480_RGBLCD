#!/usr/bin/env python3
"""
ESP32-P4 JPEG解码极限测试
使用预编码JPEG帧，绕过PC端编码瓶颈，测试ESP32的JPEG解码极限
"""

import usb.core
import usb.util
import struct
import time
import os
import glob

# USB设备参数
VID = 0x303A
PID = 0x2986

# 屏幕参数
WIDTH = 800
HEIGHT = 480

# 图像类型
UDISP_TYPE_JPG = 3

# 测试模式
MODE_UNLIMITED = 0   # 全速发送
MODE_FPS_LIMITED = 1  # 限制帧率发送


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
        return False


def load_jpeg_frames(frames_dir, max_frames=None):
    """加载所有JPEG帧"""
    pattern = os.path.join(frames_dir, "output_*.jpg")
    files = sorted(glob.glob(pattern))

    if max_frames:
        files = files[:max_frames]

    frames = []
    for f in files:
        with open(f, 'rb') as fp:
            frames.append(fp.read())

    print(f"加载了 {len(frames)} 帧, 总大小: {sum(len(f) for f in frames) / 1024:.1f} KB")
    return frames


def run_unlimited_test(ep_out, frames):
    """全速发送测试 - 尽可能快地发送所有帧"""
    print(f"\n=== 全速发送测试 ({len(frames)} 帧) ===")

    sent = 0
    errors = 0
    total_bytes = 0
    start_time = time.time()

    for i, frame_data in enumerate(frames):
        ok = send_frame(ep_out, frame_data, i)
        if ok:
            sent += 1
            total_bytes += len(frame_data)
        else:
            errors += 1

        # 每秒打印一次进度
        elapsed = time.time() - start_time
        if int(elapsed) > int(elapsed - 0.1):
            actual_fps = sent / elapsed if elapsed > 0 else 0
            bw = total_bytes * 8 / elapsed / 1_000_000 if elapsed > 0 else 0
            print(f"\r  [{i+1}/{len(frames)}] fps={actual_fps:.1f} bw={bw:.1f}Mbps errors={errors}    ", end='', flush=True)

    elapsed = time.time() - start_time
    actual_fps = sent / elapsed if elapsed > 0 else 0
    bw = total_bytes * 8 / elapsed / 1_000_000 if elapsed > 0 else 0

    print(f"\n  发送完成: {sent} 帧, {elapsed:.2f}秒, 平均 {actual_fps:.1f} fps, 带宽 {bw:.1f} Mbps, 错误 {errors}")

    return sent, errors, elapsed, bw


def run_fps_limit_test(ep_out, frames, target_fps):
    """限帧率测试"""
    print(f"\n=== 限制帧率测试: {target_fps} fps ===")

    interval = 1.0 / target_fps
    frame_id = 0
    sent = 0
    errors = 0
    total_bytes = 0
    last_send = time.time()
    start_time = time.time()

    while frame_id < len(frames):
        now = time.time()

        if now - last_send >= interval:
            ok = send_frame(ep_out, frames[frame_id], frame_id)
            if ok:
                sent += 1
                total_bytes += len(frames[frame_id])
            else:
                errors += 1

            frame_id += 1
            last_send = now

        # 每秒打印
        elapsed = time.time() - start_time
        if int(elapsed) > int(elapsed - 0.1) and frame_id > 0:
            actual_fps = sent / elapsed
            bw = total_bytes * 8 / elapsed / 1_000_000
            print(f"\r  [{frame_id}/{len(frames)}] actual={actual_fps:.1f}fps target={target_fps}fps bw={bw:.1f}Mbps    ", end='', flush=True)

        time.sleep(0.0001)

    elapsed = time.time() - start_time
    actual_fps = sent / elapsed if elapsed > 0 else 0
    bw = total_bytes * 8 / elapsed / 1_000_000 if elapsed > 0 else 0

    print(f"\n  完成: {sent} 帧, {elapsed:.2f}秒, 实际 {actual_fps:.1f} fps, 带宽 {bw:.1f} Mbps, 错误 {errors}")

    return sent, errors, elapsed, actual_fps


def run_stress_test(ep_out, frames):
    """逐步提高帧率的压力测试"""
    print("=" * 60)
    print("ESP32-P4 JPEG解码极限测试")
    print(f"预编码帧: {len(frames)} 帧")
    print("=" * 60)

    results = []

    # 先全速测试一次看看极限
    print("\n>>> 阶段1: 全速发送测试 (测ESP32极限接收能力)")
    sent, errors, elapsed, bw = run_unlimited_test(ep_out, frames)
    max_fps_estimate = sent / elapsed if elapsed > 0 else 0
    print(f"  全速极限约: {max_fps_estimate:.1f} fps")

    # 等待几秒让ESP32缓冲清空
    print("\n等待ESP32处理缓冲...")
    time.sleep(3)

    # 限帧率测试
    print("\n>>> 阶段2: 限帧率测试")
    test_fps = [10, 20, 30, 45, 60, 90, 120]

    for target in test_fps:
        if target > max_fps_estimate * 1.5:
            print(f"\n跳过 {target} fps (超出估计极限)")
            continue

        print("\n等待缓冲清空...")
        time.sleep(2)

        sent, errors, elapsed, actual_fps = run_fps_limit_test(ep_out, frames, target)
        results.append({
            'target': target,
            'actual': actual_fps,
            'errors': errors,
            'bandwidth': sent * sum(len(f) for f in frames[:sent]) / sent * 8 / elapsed / 1_000_000 if sent > 0 else 0
        })

        if errors > sent * 0.2:
            print(f"  [警告] 错误率 {(errors/sent)*100:.1f}%, 可能接近极限")
            if errors > sent * 0.5:
                print(f"  停止测试")
                break

    # 汇总
    print("\n" + "=" * 60)
    print("结果汇总")
    print("=" * 60)
    print(f"{'目标fps':>8} {'实际fps':>8} {'错误数':>8}")
    print("-" * 40)
    for r in results:
        status = "OK" if r['errors'] < r['actual'] * 0.1 else "WARN"
        print(f"{r['target']:>8} {r['actual']:>8.1f} {r['errors']:>8} {status}")

    return results


def main():
    frames_dir = os.path.join(os.path.dirname(__file__), "jpeg_frames")
    if not os.path.exists(frames_dir):
        print(f"未找到帧目录: {frames_dir}")
        return

    ep_out = find_usb_device()
    if not ep_out:
        return

    # 加载所有帧
    frames = load_jpeg_frames(frames_dir)
    if not frames:
        print("没有加载到帧!")
        return

    print("\n请观察ESP32串口日志中的 'Input fps' 和 'Display fps'")
    print("按 Ctrl+C 停止测试\n")
    time.sleep(2)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=int, default=0, help='指定帧率测试 (0=压力测试)')
    args = parser.parse_args([])

    if args.fps > 0:
        # 持续限帧率发送模式 - 直到 Ctrl+C
        print(f"\n=== 持续 {args.fps} fps 限帧率发送测试 ===")
        print("按 Ctrl+C 停止\n")
        frame_id = 0
        interval = 1.0 / args.fps
        last_send = time.time()
        sent = 0
        start_time = time.time()
        try:
            while True:
                now = time.time()
                if now - last_send >= interval:
                    idx = frame_id % len(frames)
                    ok = send_frame(ep_out, frames[idx], frame_id)
                    if ok:
                        sent += 1
                    frame_id += 1
                    last_send = now
                if now - start_time >= 1.0:
                    actual_fps = sent / (now - start_time)
                    print(f"\r  target={args.fps}fps actual={actual_fps:.1f}fps frames={frame_id}  ", end='', flush=True)
                    sent = 0
                    start_time = now
                time.sleep(0.0001)
        except KeyboardInterrupt:
            print(f"\n\n总发送 {frame_id} 帧")
    else:
        run_stress_test(ep_out, frames)


if __name__ == '__main__':
    main()
