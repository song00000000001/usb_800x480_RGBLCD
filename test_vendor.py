#!/usr/bin/env python3
"""
ESP32-P4 USB 扩展屏测试脚本
通过 Vendor USB 发送图像数据到 ESP32-P4
"""

import usb.core
import usb.util
import struct
import time

# USB设备参数
VID = 0x303a
PID = 0x2986

# 屏幕参数
WIDTH = 800
HEIGHT = 480

# 图像类型
UDISP_TYPE_RGB565 = 0
UDISP_TYPE_RGB888 = 1
UDISP_TYPE_YUV420 = 2
UDISP_TYPE_JPG = 3

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

def create_frame_header(width, height, payload_size, frame_type=UDISP_TYPE_RGB565, frame_id=0):
    """
    创建帧头 - 填充到512字节以匹配USB包大小
    """
    # frame_id (10位) + payload_total (22位) 打包成一个32位值
    frame_id_payload = ((frame_id & 0x3FF) | ((payload_size & 0x3FFFFF) << 10))

    # 打包帧头 (小端序) - 不含CRC
    header = struct.pack(
        '<BBHHHHI',  # 小端序: B=uint8, H=uint16, I=uint32
        frame_type,  # type
        0,           # cmd
        0,           # x
        0,           # y
        width,       # width
        height,      # height
        frame_id_payload  # frame_id(10bit) + payload_total(22bit)
    )

    # 计算CRC
    crc = crc16(header)

    # 最终帧头: CRC + 其他字段
    full_header = struct.pack('<H', crc) + header

    # 填充到512字节（USB包大小）
    padding_size = 512 - len(full_header)
    full_header += b'\x00' * padding_size

    print(f"帧头构造:")
    print(f"  type={frame_type}, cmd=0, x=0, y=0, w={width}, h={height}")
    print(f"  payload_size={payload_size}, frame_id={frame_id}")
    print(f"  CRC=0x{crc:04X}")
    print(f"  帧头长度: {len(full_header)} 字节 (填充后)")
    print(f"  前32字节: {full_header[:32].hex()}")

    return full_header

def create_rgb565_test_image(width, height, r=31, g=63, b=31):
    """创建纯色RGB565测试图像"""
    # RGB565: R(5) G(6) B(5)
    pixel = ((r & 0x1F) << 11) | ((g & 0x3F) << 5) | (b & 0x1F)
    return struct.pack('<H', pixel) * (width * height)

def main():
    # 查找设备
    print(f"查找设备 VID=0x{VID:04x}, PID=0x{PID:04x}")
    dev = usb.core.find(idVendor=VID, idProduct=PID)

    if dev is None:
        print("未找到设备!")
        return

    print(f"找到设备: {dev}")

    # 配置设备
    try:
        # 释放内核驱动
        for cfg in dev:
            for intf in cfg:
                if dev.is_kernel_driver_active(intf.bInterfaceNumber):
                    try:
                        dev.detach_kernel_driver(intf.bInterfaceNumber)
                        print(f"释放内核驱动: 接口 {intf.bInterfaceNumber}")
                    except usb.core.USBError as e:
                        print(f"无法释放内核驱动: {e}")

        dev.set_configuration()
    except usb.core.USBError as e:
        print(f"配置设备失败: {e}")
        return

    # 获取配置
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]

    # 查找端点
    ep_out = usb.util.find_descriptor(
        intf,
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
    )

    if ep_out is None:
        print("未找到OUT端点!")
        return

    print(f"OUT端点: 0x{ep_out.bEndpointAddress:02x}")

    # 创建测试图像
    payload_size = WIDTH * HEIGHT * 2  # RGB565

    print(f"\n发送测试画面 {WIDTH}x{HEIGHT} RGB565...")
    print(f"数据大小: {payload_size} 字节")

    # 测试颜色列表
    colors = [
        ("红色", 31, 0, 0),
        ("绿色", 0, 63, 0),
        ("蓝色", 0, 0, 31),
        ("黄色", 31, 63, 0),
        ("白色", 31, 63, 31),
    ]

    for i, (name, r, g, b) in enumerate(colors):
        print(f"\n发送 {name} ({i+1}/{len(colors)})...")

        # 创建帧头
        header = create_frame_header(WIDTH, HEIGHT, payload_size, UDISP_TYPE_RGB565, i)

        # 创建图像数据
        image_data = create_rgb565_test_image(WIDTH, HEIGHT, r, g, b)

        # 发送数据
        try:
            # 发送帧头（已填充到512字节）
            print(f"  发送帧头...")
            ep_out.write(header)

            # 发送图像数据（使用较大chunk提高效率）
            print(f"  发送图像数据: {len(image_data)} 字节")
            chunk_size = 16384  # 每次发送16KB，提高USB传输效率
            total_sent = 0
            for offset in range(0, len(image_data), chunk_size):
                chunk = image_data[offset:offset + chunk_size]
                ep_out.write(chunk)
                total_sent += len(chunk)

            print(f"  发送完成 ({total_sent} 字节)")
            time.sleep(2.0)  # 等待ESP32处理并显示

        except usb.core.USBError as e:
            print(f"  发送失败: {e}")
            break

    print("\n测试完成!")

if __name__ == '__main__':
    main()