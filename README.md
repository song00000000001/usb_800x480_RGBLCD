# ESP32-P4 USB 外扩副屏项目

## 项目概述

本项目基于 **ESP32-P4** 实现 USB 外扩副屏功能，通过 USB OTG 将开发板作为 USB Device 连接主机（PC），主机端运行 Python 投屏脚本将屏幕内容实时传输到副屏显示。

### 系统架构

```
┌─────────────┐      USB OTG      ┌─────────────────┐
│   PC 主机   │ ────────────────→ │  ESP32-P4 副屏  │
│             │   512字节帧头     │  800×480 LCD   │
│ Python 投屏 │   + JPEG/RGB 数据 │  RGB565 显示    │
└─────────────┘                  └─────────────────┘
```

### 核心功能

| 功能 | 说明 |
|------|------|
| **USB Vendor 协议** | 512 字节自定义帧头，支持 RGB565/RGB888/YUV420/JPEG 数据格式 |
| **JPEG 压缩传输** | 推荐使用 JPEG 格式，降低 USB 带宽占用 |
| **帧缓冲管理** | 8 帧缓冲池，支持丢帧策略和 FPS 统计 |
| **UAC 音频** | 24kHz 单声道，双向传输（播放+录音） |
| **即插即用** | USB 枚举后自动识别为副屏设备 |

---

## 硬件配置

| 组件 | 型号/规格 | 说明 |
|------|----------|------|
| 主控芯片 | ESP32-P4 | 支持 USB OTG，USB 2.0 High Speed (UTMI PHY) |
| 显示模块 | 4.3寸 RGB LCD | 800×480 分辨率 |
| 触摸屏 | GT9xxx | 电容触摸屏，I2C 接口（已禁用触摸上报） |
| 音频Codec | ES8388 | I2S 接口 |
| IO扩展 | XL9555 | I2C 接口 |

---

## USB 传输协议

### Vendor 数据包格式（512 字节帧头）

```c
typedef struct {
    uint8_t  sync[4];       // 同步标记 "UDSP"
    uint16_t crc16;         // CRC16 校验（MODBUS标准）
    uint8_t  type;          // 0=RGB565, 1=RGB888, 2=YUV420, 3=JPEG
    uint8_t  cmd;           // 命令
    uint16_t x;             // X 偏移
    uint16_t y;             // Y 偏移
    uint16_t width;         // 宽度
    uint16_t height;        // 高度
    uint32_t frame_id: 10;  // 帧ID
    uint32_t payload_total: 22; // 总长度
} __attribute__((packed)) udisp_frame_header_t;
```

### 支持的数据类型

- `UDISP_TYPE_RGB565 (0)` - 原始 RGB565 数据
- `UDISP_TYPE_RGB888 (1)` - RGB888 数据
- `UDISP_TYPE_YUV420 (2)` - YUV420 数据
- `UDISP_TYPE_JPG (3)` - JPEG 压缩数据（推荐，降低传输带宽）

### 帧同步机制

- 同步标记：`"UDSP"` (4字节)
- CRC16 校验：从 type 字段开始的 14 字节数据
- 帧头跨包处理：支持帧头不完整时缓存后续数据
- Dimension mismatch 时自动跳过完整帧

---

## 目录结构

```
.
├── main/                           # 主程序
│   ├── main.c                      # 程序入口
│   ├── CMakeLists.txt              # 组件构建配置
│   ├── idf_component.yml          # 组件依赖声明
│   ├── APP/                        # 应用层
│   │   ├── app_usb.c/h             # USB 初始化
│   │   ├── app_lcd.c/h             # LCD 显示驱动
│   │   ├── app_hid.c/h             # HID（已禁用触摸）
│   │   ├── app_vendor.c/h          # Vendor 数据传输
│   │   ├── app_uac.c/h             # UAC 音频
│   │   ├── usb_frame.c/h           # 帧缓冲管理
│   │   ├── usb_descriptors.c/h     # USB 描述符
│   │   ├── uac_descriptors.h       # UAC 音频描述符
│   │   ├── tusb_config.h           # TinyUSB 配置
│   │   └── app_config.h            # 应用配置
│   └── UAC/                        # UAC 音频配置
│       ├── uac_config.h
│       ├── tusb_config_uac.h
│       ├── usb_device_uac.c/h
│       └── uac_descriptors.h
├── components/                     # 组件
│   ├── BSP/                        # 板级支持包
│   │   ├── LCD/                    # LCD 驱动
│   │   ├── ES8388/                # 音频 Codec
│   │   ├── MYI2S/                  # I2S 接口
│   │   ├── MYIIC/                  # I2C 接口
│   │   ├── XL9555/                 # IO 扩展芯片
│   │   └── LED/                    # LED 驱动
│   └── Middlewares/               # 中间件
├── screen_stream_portal.py         # 无闪白投屏脚本（Portal ScreenCast API）
├── screen_stream_mutter.py          # Mutter 投屏脚本
├── window_crop_helper.py            # 窗口裁剪辅助脚本
├── test_vendor.py                  # Vendor 模式测试脚本
└── build/                          # 编译输出目录
```

---

## IO 引脚分配

### GPIO 直接控制

| 功能 | GPIO | 说明 |
|------|------|------|
| LED0 | GPIO 51 | 状态指示灯 |
| LCD 背光 | GPIO 53 | 背光控制 |
| LCD 复位 | GPIO 52 | 复位信号 |

### I2C 接口 (I2C_NUM_0)

| 信号 | GPIO |
|------|------|
| SCL | GPIO 32 |
| SDA | GPIO 33 |

**I2C 设备地址**:
- XL9555: 0x24
- ES8388: 0x10
- GT9xxx: 0x14

### I2S 接口 (音频)

| 信号 | GPIO |
|------|------|
| MCLK | GPIO 46 |
| BCK | GPIO 47 |
| WS | GPIO 48 |
| DO | GPIO 49 |
| DI | GPIO 50 |

### RGB LCD 接口 (16 位 RGB565)

| 信号 | GPIO |
|------|------|
| PCLK | GPIO 20 |
| DE | GPIO 22 |

**数据线**: GPIO 3-18（16 位）

### 触摸屏接口

| 信号 | GPIO |
|------|------|
| TP_INT | GPIO 21 |
| TP_RST | GPIO 45 |

---

## 编译与烧录

```bash
# 设置 ESP-IDF 环境
source $IDF_PATH/export.sh

# 编译
idf.py build

# 烧录
idf.py -p /dev/ttyUSB0 flash

# 监视串口输出
idf.py -p /dev/ttyUSB0 monitor
```

---

## Python 屏幕投屏

### screen_stream_portal.py - 无闪白版（推荐）

使用 Portal ScreenCast API，支持全屏/窗口投屏，无闪白效果：
- JPEG 压缩传输（默认质量 70%）
- 支持全屏/窗口模式/手动裁剪
- 支持屏幕旋转

```bash
# 全屏投屏
python3 screen_stream_portal.py

# 窗口选择模式
python3 screen_stream_portal.py -w

# 带旋转
python3 screen_stream_portal.py -r 90

# 手动裁剪区域
python3 screen_stream_portal.py --crop 100,50,640,480

# 单帧截屏测试
python3 screen_stream_portal.py -s
```

### screen_stream_mutter.py - Mutter 版

使用 Mutter ScreenCast API（Linux Gnome 环境）：

```bash
python3 screen_stream_mutter.py
```

---

## 依赖组件

### ESP-IDF 组件

| 组件 | 版本 | 说明 |
|------|------|------|
| leeebo/tinyusb_src | ^0.16.0~6 | TinyUSB 协议栈 |
| espressif/esp_codec_dev | ^1.3.1 | 音频编解码 |
| chmorgan/esp-audio-player | ^1.0.7 | 音频播放 |
| chmorgan/esp-libhelix-mp3 | ^1.0.3 | MP3 解码 |
| chmorgan/esp-file-iterator | ^1.0.0 | 文件迭代器 |
| espressif/cmake_utilities | ^1.0.0 | CMake 工具 |

### Python 依赖

| 组件 | 版本 | 说明 |
|------|------|------|
| usb | ^2.17.0 | USB 通信 |
| dbus | ^1.0.7 | DBus 通信（Portal 需要） |
| numpy | - | 数值计算 |
| Pillow | - | 图像处理 |
| GObject introspection | - | GStreamer 绑定 |
| GStreamer | - | 媒体框架 |
| gi-cairo | - | Cairo 绑定 |

---

## 开发环境

- **ESP-IDF**: v6.1
- **目标芯片**: ESP32-P4
- **LCD 面板**: 4.3 寸 800×480 RGB LCD
- **Python**: 3.x
- **主机系统**: Ubuntu 24.04 / Linux (PipeWire/Portal/D-Bus)

### USB VID/PID

- **VID**: 0x303A
- **PID**: 0x2986
- **产品名称**: DNESP32-P4 Board

---

## 技术支持

- 在线视频: www.yuanzige.com
- 技术论坛: www.openedv.com
- 公司网址: www.alientek.com
- 购买地址: openedv.taobao.com
