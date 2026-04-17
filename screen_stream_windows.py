import usb.core
import usb.util
import struct
import time
import sys
import argparse
import numpy as np
import queue
import pygetwindow as gw
from mss import mss
from PIL import Image
import ctypes

# 解决 Windows 高 DPI 缩放导致的截屏偏差
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# USB设备参数 (保持不变)
VID = 0x303a
PID = 0x2986
WIDTH = 800
HEIGHT = 480
UDISP_TYPE_JPG = 3
JPEG_QUALITY = 75

# 全局变量
ep_out = None

def get_windows():
    """获取所有可见窗口"""
    return [w for w in gw.getAllWindows() if w.title and w.width > 0]

def select_window_interactive():
    """交互式选择窗口"""
    windows = get_windows()
    print("\n可用窗口:")
    for i, w in enumerate(windows):
        print(f"  [{i+1}] {w.title} ({w.width}x{w.height})")
    print("  [0] 全屏模式")
    
    try:
        choice = int(input("\n请选择编号: "))
        if choice == 0: return None
        return windows[choice-1]
    except:
        return None

def crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1: crc = (crc >> 1) ^ 0xA001
            else: crc >>= 1
    return crc

def create_frame_header(width, height, payload_size, frame_type, frame_id):
    SYNC_MARKER = b'UDSP'
    frame_id_payload = ((frame_id & 0x3FF) | ((payload_size & 0x3FFFFF) << 10))
    header_data = struct.pack('<BBHHHHI', frame_type, 0, 0, 0, width, height, frame_id_payload)
    crc = crc16(header_data)
    full_header = struct.pack('<H', crc) + header_data
    return SYNC_MARKER + full_header + bytes(512 - len(SYNC_MARKER) - len(full_header))

def find_usb_device():
    dev = usb.core.find(idVendor=VID, idProduct=PID)
    if dev is None:
        print("未找到设备! 请确保已使用 Zadig 安装 WinUSB 驱动。")
        return None
    dev.set_configuration()
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]
    return usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

def send_frame(img, frame_id):
    global ep_out
    if ep_out is None: return False
    
    # 调整大小以适应屏幕
    img = img.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
    
    import io
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=JPEG_QUALITY)
    data = buffer.getvalue()
    
    header = create_frame_header(WIDTH, HEIGHT, len(data), UDISP_TYPE_JPG, frame_id)
    try:
        ep_out.write(header)
        chunk_size = 4096
        for offset in range(0, len(data), chunk_size):
            ep_out.write(data[offset:offset + chunk_size])
        return True, len(data)
    except Exception as e:
        print(f"发送失败: {e}")
        return False, 0

def main():
    global ep_out
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--window', action='store_true', help='窗口模式')
    args = parser.parse_args()

    ep_out = find_usb_device()
    if not ep_out: return

    selected_win = None
    if args.window:
        selected_win = select_window_interactive()

    sct = mss()
    frame_id = 0
    last_time = time.time()
    
    print("开始投屏... 按 Ctrl+C 退出")
    
    try:
        while True:
            # 确定截屏区域
            if selected_win:
                # 检查窗口是否还存在
                if not selected_win.isActive: 
                    # 尝试重新获取位置
                    monitor = {"top": selected_win.top, "left": selected_win.left, 
                               "width": selected_win.width, "height": selected_win.height}
                else:
                    monitor = {"top": selected_win.top, "left": selected_win.left, 
                               "width": selected_win.width, "height": selected_win.height}
            else:
                monitor = sct.monitors[1] # 主显示器全屏

            # 截屏并转换
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # 发送
            ok, size = send_frame(img, frame_id)
            if ok:
                frame_id += 1
            
            # FPS 控制与显示
            if frame_id % 10 == 0:
                now = time.time()
                fps = 10 / (now - last_time)
                print(f"当前 FPS: {fps:.1f}", end='\r')
                last_time = now
                
    except KeyboardInterrupt:
        print("\n已停止")

if __name__ == '__main__':
    main()