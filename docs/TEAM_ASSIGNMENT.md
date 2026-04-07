# ESP32-P4 USB 外扩副屏项目 - 团队工作分配方案

> **项目类型**: 嵌入式固件开发项目
> **团队规模**: 5人
> **项目状态**: 核心功能开发完成
> **技术栈**: ESP-IDF 6.1 + TinyUSB + FreeRTOS + C

---

## 一、项目概述

### 1.1 项目目标

开发基于 **ESP32-P4** 的 USB 外扩副屏设备，实现以下核心功能：

| 功能模块 | 描述 | 状态 |
|----------|------|------|
| USB Device | 作为USB设备连接PC | 已完成 |
| RGB LCD 显示 | 800x480 分辨率显示 | 已完成 |
| Vendor模式 | Windows专用驱动模式 | 已完成 |
| JPEG解码 | 硬件JPEG解码显示 | 已完成 |
| UAC音频 | USB Audio双向传输 | 已完成 |

### 1.2 系统架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PC 端 (USB Host)                                │
│                    ┌─────────────┐                                          │
│                    │ AIRI App    │                                          │
│                    │ (Electron)  │                                          │
│                    └──────┬──────┘                                          │
└───────────────────────────┼─────────────────────────────────────────────────┘
                            │ USB
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ESP32-P4 固件架构                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                          应用层 (main/APP)                            │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │  │
│  │  │ app_usb.c   │ │ app_lcd.c   │ │ app_uac.c   │ │ usb_frame.c     │ │  │
│  │  │ USB管理     │ │ JPEG解码    │ │ UAC音频     │ │ 帧缓冲管理      │ │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────┘ │  │
│  │  ┌─────────────┐                                                       │  │
│  │  │ app_vendor.c│                                                       │  │
│  │  │ Vendor数据  │                                                       │  │
│  │  └─────────────┘                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                       USB协议层 (TinyUSB)                             │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────────────────────┐               │  │
│  │  │ Vendor  │ │   UAC   │ │ usb_descriptors         │               │  │
│  │  │ 自定义类 │ │ 音频流  │ │ USB描述符               │               │  │
│  │  └─────────┘ └─────────┘ └─────────────────────────┘               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        BSP驱动层 (components/BSP)                     │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────────┐                            │  │
│  │  │ LCD驱动 │ │ ES8388  │ │ I2C/I2S/LED │                            │  │
│  │  │ RGB/MIPI│ │ 音频Codec│ │ 通信接口    │                            │  │
│  │  └─────────┘ └─────────┘ └─────────────┘                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         ESP-IDF 系统层                                │  │
│  │      FreeRTOS │ GPIO │ I2C │ I2S │ LCD │ USB OTG │ SPIRAM │ NVS   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            硬件层                                            │
│  ┌────────────┐  ┌────────────┐                                          │
│  │ 800x480   │  │ ES8388     │                                          │
│  │ RGB LCD    │  │ 音频Codec  │                                          │
│  └────────────┘  └────────────┘                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 数据流向

```
┌─────────────┐                                              ┌─────────────┐
│   PC 端     │                                              │   PC 端     │
│  图像数据   │                                              │  音频数据   │
└──────┬──────┘                                              └──────┬──────┘
       │                                                            │
       │ ① JPEG/RGB565 压缩图像                                    │ ② UAC音频
       │ (Vendor 模式)                                             │ (录音/播放)
       ▼                                                            │
┌─────────────┐    ③ JPEG解码    ┌─────────────┐                   │
│ USB 接收    │ ──────────────► │ 帧缓冲区    │                   │
│ Vendor模式  │                  │ (PSRAM)     │                   │
└─────────────┘                  └──────┬──────┘                   │
                                        │                          │
                                        │ ④ RGB565 输出            │
                                        ▼                          │
                                 ┌─────────────┐                   │
                                 │  RGB LCD    │                   │
                                 │  800x480    │                   │
                                 └─────────────┘                   │
```

---

## 二、USB协议规范

### 2.1 帧头格式 (512字节)

| 偏移 | 大小 | 字段 | 描述 |
|------|------|------|------|
| 0-3 | 4 | sync | "UDSP" 同步标记 |
| 4-5 | 2 | crc16 | MODBUS CRC16 (多项式 0xA001) |
| 6 | 1 | type | 0=RGB565, 1=RGB888, 2=YUV420, 3=JPEG |
| 7 | 1 | cmd | 命令 (0) |
| 8-9 | 2 | x | X偏移 (0) |
| 10-11 | 2 | y | Y偏移 (0) |
| 12-13 | 2 | width | 帧宽度 |
| 14-15 | 2 | height | 帧高度 |
| 16-19 | 4 | frame_info | frame_id(10 bits) \| (payload_total(22 bits) << 10) |

### 2.2 CRC16实现 (MODBUS)

```c
static uint16_t calculate_crc16(const uint8_t *data, size_t len)
{
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++)
    {
        crc ^= data[i];
        for (int j = 0; j < 8; j++)
        {
            if (crc & 1)
                crc = (crc >> 1) ^ 0xA001;
            else
                crc >>= 1;
        }
    }
    return crc;
}
```

### 2.3 数据类型

| 类型 | 值 | 描述 |
|------|-------|------|
| RGB565 | 0 | 16-bit BGR (5-6-5) |
| RGB888 | 1 | 24-bit RGB |
| YUV420 | 2 | YUV格式 |
| JPEG | 3 | JPEG压缩（推荐） |

### 2.4 像素格式: BGR565

**重要**: ESP32-P4固件LCD驱动期望 **BGR565** 格式，不是RGB565。

发送原始RGB565帧时，R和B组件必须交换：
```c
const b5 = (color.b >> 3) & 0x1F
const g6 = (color.g >> 2) & 0x3F
const r5 = (color.r >> 3) & 0x1F
const bgr565 = (b5 << 11) | (g6 << 5) | r5
```

---

## 三、固件架构

### 3.1 主任务流程

```
app_main()
    ├── nvs_flash_init()          # NVS初始化
    ├── led_init()                 # LED初始化
    ├── myiic_init()               # I2C总线初始化
    ├── es8388_init()              # ES8388音频Codec初始化
    ├── myi2s_init()               # I2S接口初始化
    ├── app_usb_init()             # USB设备栈初始化
    │   ├── usb_phy_init()        # USB PHY初始化
    │   ├── tusb_init()           # TinyUSB初始化
    │   ├── app_vendor_init()     # Vendor模式初始化
    │   ├── app_uac_init()        # UAC音频初始化
    │   └── xTaskCreate(tusb_device_task)
    └── app_lcd_init()            # LCD初始化和JPEG解码器
```

### 3.2 Vendor数据接收流程

```
tud_vendor_rx_cb()
    ├── tud_vendor_n_available()  # 检查接收数据
    ├── tud_vendor_n_read()       # 读取数据
    ├── Search "UDSP" sync marker
    ├── Validate CRC16
    ├── Parse frame header (512 bytes)
    ├── Check dimension match (800x480)
    └── buffer_fill()
        └── frame_add_data()
        └── frame_send_filled()

transfer_task()
    ├── frame_get_filled()        # 等待完整帧
    └── app_lcd_draw()            # 显示帧
        └── jpeg_decoder_process()
        └── esp_lcd_panel_draw_bitmap()
```

### 3.3 帧缓冲管理

```
frame_allocate(8, JPEG_BUFFER_SIZE)
    ├── xQueueCreate(empty_fb_queue, 8)
    ├── xQueueCreate(filled_fb_queue, 8)
    └── 8x frame_t allocated
```

---

## 四、项目当前状态

### 4.1 固件侧已完成模块

| 模块 | 文件 | 功能 | 状态 |
|------|------|------|------|
| USB核心 | `main/APP/app_usb.c` | USB PHY初始化、TinyUSB集成 | 已完成 |
| Vendor模式 | `main/APP/app_vendor.c` | 数据接收、帧解析、CRC校验 | 已完成 |
| USB描述符 | `main/APP/usb_descriptors.c` | 设备/配置/字符串描述符 | 已完成 |
| TinyUSB配置 | `main/APP/tusb_config.h` | USB HS/Vendor配置 | 已完成 |
| LCD驱动 | `components/BSP/LCD/lcd.c` | RGB LCD驱动、多面板支持 | 已完成 |
| RGB LCD | `components/BSP/LCD/rgblcd.c` | RGB面板时序配置 | 已完成 |
| MIPI LCD | `components/BSP/LCD/mipi_lcd.c` | MIPI面板驱动(备用) | 已完成 |
| JPEG解码 | `main/APP/app_lcd.c` | 硬件JPEG解码、显示输出 | 已完成 |
| 帧缓冲管理 | `main/APP/usb_frame.c` | 多缓冲机制、帧同步 | 已完成 |
| UAC音频 | `main/UAC/usb_device_uac.c` | UAC设备驱动 | 已完成 |
| UAC应用 | `main/APP/app_uac.c` | ES8388集成、I2S音频 | 已完成 |
| I2C驱动 | `components/BSP/MYIIC/myiic.c` | I2C主机总线 | 已完成 |
| I2S驱动 | `components/BSP/MYI2S/myi2s.c` | I2S音频接口 | 已完成 |
| LED驱动 | `components/BSP/LED/led.c` | LED状态指示 | 已完成 |
| ES8388驱动 | `components/BSP/ES8388/es8388.c` | 音频Codec | 已完成 |

### 4.2 PC端已完成模块 (AIRI Electron App)

| 模块 | 文件 | 功能 | 状态 |
|------|------|------|------|
| Frame Capture | `packages/stage-ui/src/composables/frame-capture.ts` | WebGL canvas帧捕获，BGR565支持 | 已完成 |
| USB Stream | `packages/stage-ui/src/composables/use-usb-display-stream.ts` | AIRI视频流composable | 已完成 |
| IPC Wrapper | `apps/stage-tamagotchi/src/renderer/composables/use-usb-display.ts` | Renderer IPC封装 | 已完成 |
| USB Service | `apps/stage-tamagotchi/src/main/services/usb-display/index.ts` | USB显示服务，协议实现 | 已完成 |
| UI Toggle | `apps/stage-tamagotchi/src/renderer/components/UsbDisplayToggle.vue` | USB显示UI开关组件 | 已完成 |
| Test Script | `apps/stage-tamagotchi/scripts/test-usb-display.ts` | RGB565测试脚本 | 已完成 |

---

## 五、团队成员角色分配

### 5.1 成员A - 项目架构师 & USB协议栈负责人

**角色定位**: 技术负责人，USB核心开发，系统集成

**核心职责**:
- USB PHY初始化和时钟配置
- TinyUSB框架集成和维护
- Vendor模式数据接收和帧解析
- USB描述符管理和维护
- 系统集成和任务调度

**当前交付物**:
- USB初始化模块 (`app_usb.c`)
- Vendor模式实现 (`app_vendor.c`)
- USB描述符配置 (`usb_descriptors.c`)
- TinyUSB配置 (`tusb_config.h`)

---

### 5.2 成员B - 显示子系统负责人

**角色定位**: LCD驱动开发，图像处理核心

**核心职责**:
- RGB LCD驱动开发和维护
- 多面板自动识别支持
- JPEG解码和显示输出
- 帧缓冲管理和优化
- MIPI LCD备用方案

**当前交付物**:
- LCD驱动模块 (`lcd.c/h`, `rgblcd.c/h`)
- JPEG解码显示 (`app_lcd.c`)
- 帧缓冲管理 (`usb_frame.c/h`)

**技术亮点**:
- 支持多种面板自动识别 (0x4342/0x7084/0x7016/0x7018/0x4384/0x1018/0x4350)
- 硬件JPEG解码
- 单缓冲机制避免撕裂

---

### 5.3 成员C - BSP驱动负责人

**角色定位**: 底层硬件驱动，通信接口开发

**核心职责**:
- I2C/I2S总线驱动开发和维护
- LED控制驱动
- GPIO基础管理
- BSP模块集成测试

**当前交付物**:
- I2C总线驱动 (`myiic.c/h`)
- I2S音频接口 (`myi2s.c/h`)
- LED驱动 (`led.c/h`)

---

### 5.4 成员D - 音频子系统负责人

**角色定位**: 音频驱动开发

**核心职责**:
- UAC USB Audio设备驱动
- ES8388与I2S集成配置
- 音频数据流管理

**当前交付物**:
- UAC设备驱动 (`usb_device_uac.c/h`)
- UAC应用层 (`app_uac.c/h`)
- UAC配置文件 (`uac_config.h`, `tusb_config_uac.h`)
- ES8388 Codec (`es8388.c/h`)

**技术亮点**:
- 支持24kHz采样率
- 16位单声道音频
- Speaker和Mic双向传输
- 音量/静音控制回调

---

### 5.5 成员E - PC端开发负责人

**角色定位**: AIRI Electron App开发

**核心职责**:
- AIRI Electron App USB显示集成
- WebGL canvas帧捕获优化
- USB协议通信调试
- PC端功能扩展

**当前交付物**:
- Frame Capture模块 (`frame-capture.ts`)
- USB Stream服务 (`use-usb-display-stream.ts`)
- IPC通信封装 (`use-usb-display.ts`)
- USB显示服务 (`usb-display/index.ts`)
- UI组件 (`UsbDisplayToggle.vue`)
- 测试脚本 (`test-usb-display.ts`)

**技术要求**:
- 熟悉 Electron/Node.js USB通信
- 熟悉 TypeScript/Vue 开发
- 熟悉 WebGL canvas帧捕获
- 熟悉 libusb 或 native USB API

---

## 六、文件清单与责任分配

### 6.1 固件文件

| 文件路径 | 负责人 | 主要功能 |
|----------|--------|----------|
| `main/main.c` | 成员A | 程序入口、系统初始化 |
| `main/APP/app_usb.c/h` | 成员A | USB设备栈管理 |
| `main/APP/app_vendor.c/h` | 成员A | Vendor自定义设备类 |
| `main/APP/usb_descriptors.c/h` | 成员A | USB描述符定义 |
| `main/APP/tusb_config.h` | 成员A | TinyUSB配置 |
| `main/APP/app_lcd.c/h` | 成员B | LCD应用层、JPEG解码 |
| `main/APP/usb_frame.c/h` | 成员B | 帧缓冲管理 |
| `main/APP/app_uac.c/h` | 成员D | UAC应用层 |
| `main/APP/app_config.h` | 成员A | 应用配置参数 |
| `main/UAC/usb_device_uac.c/h` | 成员D | UAC设备驱动 |
| `main/UAC/uac_config.h` | 成员D | UAC配置参数 |
| `main/UAC/tusb_config_uac.h` | 成员D | TinyUSB UAC配置 |
| `main/UAC/uac_descriptors.h` | 成员D | UAC描述符 |
| `components/BSP/LCD/lcd.c/h` | 成员B | LCD底层驱动 |
| `components/BSP/LCD/rgblcd.c/h` | 成员B | RGB LCD驱动 |
| `components/BSP/LCD/mipi_lcd.c/h` | 成员B | MIPI LCD驱动 |
| `components/BSP/LCD/lcdfont.h` | 成员B | LCD字库 |
| `components/BSP/MYIIC/myiic.c/h` | 成员C | I2C主机驱动 |
| `components/BSP/MYI2S/myi2s.c/h` | 成员C | I2S驱动 |
| `components/BSP/LED/led.c/h` | 成员C | LED驱动 |
| `components/BSP/ES8388/es8388.c/h` | 成员D | 音频Codec驱动 |

### 6.2 PC端文件 (AIRI Electron App)

| 文件路径 | 负责人 | 主要功能 |
|----------|--------|----------|
| `packages/stage-ui/src/composables/frame-capture.ts` | 成员E | WebGL canvas帧捕获 |
| `packages/stage-ui/src/composables/use-usb-display-stream.ts` | 成员E | AIRI视频流composable |
| `apps/stage-tamagotchi/src/renderer/composables/use-usb-display.ts` | 成员E | Renderer IPC封装 |
| `apps/stage-tamagotchi/src/main/services/usb-display/index.ts` | 成员E | USB显示服务 |
| `apps/stage-tamagotchi/src/renderer/components/UsbDisplayToggle.vue` | 成员E | USB显示UI开关 |
| `apps/stage-tamagotchi/scripts/test-usb-display.ts` | 成员E | RGB565测试脚本 |
| `apps/stage-tamagotchi/scripts/send_usb_frame.py` | 成员E | Python USB发送脚本 |

---

## 七、硬件资源分配

### 7.1 GPIO资源分配表

| GPIO | 功能 | 负责模块 | 负责人 |
|------|------|----------|--------|
| GPIO3-22 | RGB LCD数据线 | LCD驱动 | 成员B |
| GPIO20 | LCD PCLK | LCD驱动 | 成员B |
| GPIO22 | LCD DE | LCD驱动 | 成员B |
| GPIO52 | LCD RST | LCD驱动 | 成员B |
| GPIO53 | LCD背光 | LCD驱动 | 成员B |
| GPIO32 | I2C SCL | I2C驱动 | 成员C |
| GPIO33 | I2C SDA | I2C驱动 | 成员C |
| GPIO46-50 | I2S音频 | I2S驱动 | 成员C |
| GPIO51 | LED | LED驱动 | 成员C |

### 7.2 I2C设备地址分配

| 设备 | I2C地址 | 负责模块 | 负责人 |
|------|---------|----------|--------|
| ES8388 | 0x10 | 音频Codec | 成员D |

### 7.3 LCD面板ID识别

| ID | 面板型号 | 分辨率 |
|----|----------|--------|
| 0x4342 | ATK-MD0430R-480272 | 480x272 |
| 0x7084 | ATK-MD0700R-800480 | 800x480 |
| 0x7016 | ATK-MD0700R-1024600 | 1024x600 |
| 0x7018 | ATK-MD0700R-1280800 | 1280x800 |
| 0x4384 | ATK-MD0430R-800480 | 800x480 |
| 0x1018 | ATK-MD1018R-1280800 | 1280x800 |
| 0x4350 | RGB 800x400 | 800x400 |

---

## 八、调试方法

### 8.1 固件调试输出

正常运行时的串口输出：
```
I (856) app_usb: USB Mount
I (860) app_usb: USB Device Stack Init Success
I (900) app_lcd: JPEG buffer allocated: 0x70000000, size=768000
I (950) transfer_task: Input fps: 15.32
I (1000) app_lcd: Display fps: 15.28
```

### 8.2 常见问题

1. **LIBUSB_ERROR_ACCESS**: 创建udev规则
   ```
   # /etc/udev/rules.d/99-esp32-p4-display.rules
   SUBSYSTEM=="usb", ATTR{idVendor}=="303a", ATTR{idProduct}=="2986", MODE="0666"
   ```

2. **颜色错误**: 检查像素格式是否为 **BGR565**

3. **设备未找到**: 检查VID/PID是否与固件配置匹配 (0x303A:0x2986)

4. **帧不显示**: 检查尺寸匹配 - 固件期望800x480

### 8.3 测试命令

```bash
# 发送RGB565测试帧 (BGR565格式)
npx tsx apps/stage-tamagotchi/scripts/test-usb-display.ts --test-frame --vid=0x303a --pid=0x2986

# 发送JPEG帧
python3 apps/stage-tamagotchi/scripts/send_usb_frame.py 0x303a 0x2986 800 480 0 "255,0,0" jpeg
```

---

## 九、代码规范

### 9.1 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 函数 | 小写+下划线 | `lcd_init()`, `app_vendor_rx_cb()` |
| 变量 | 小写+下划线 | `frame_buffer`, `jpeg_buf_size` |
| 宏定义 | 大写+下划线 | `LCD_WIDTH`, `USB_VENDOR_RX_BUFSIZE` |
| 结构体 | 小写+_t/dev | `frame_t`, `lcd_dev` |
| 全局变量 | g_前缀 | `g_back_color` |

### 9.2 文件头模板

```c
/**
 ******************************************************************************
 * @file        文件名.c
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       模块简要描述
 ******************************************************************************
 */
```

---

## 十、待优化项

1. **多面板支持**: 扩展支持1024x600及其他分辨率
2. **音频改进**: 立体声支持，更高采样率 (44.1kHz/48kHz)
3. **性能优化**: 更高帧率，更低延迟

---

> **文档版本**: V7.0
> **创建日期**: 2026-04-02
> **维护人**: 项目团队
