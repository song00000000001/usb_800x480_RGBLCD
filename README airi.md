# ESP32-P4 与 AIRI 集成开发指南

**硬件平台**: ESP32-P4 + ES8388 + RGB LCD 800×480
**AI 框架**: AIRI (赛博灵魂容器)
**更新日期**: 2026-04-02

---

## 1. 系统概述

本项目将 ESP32-P4 开发板作为 AIRI (AI VTuber 框架) 的下位机使用。通过 USB 2.0 HS 连接，ESP32-P4 承担音频输入/输出和 LCD 显示功能，PC 上的 AIRI 负责 AI 脑力（STT + LLM + TTS）。

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PC (AIRI)                                   │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────────────────┐ │
│  │ AIRI Brain   │◄─►│ Audio Pipe   │◄─►│ USB Display Service    │ │
│  │ (LLM + TTS)  │   │ (STT/TTS)    │   │ (帧传输)               │ │
│  └──────────────┘   └──────────────┘   └─────────────────────────┘ │
│                         │                        │                  │
│                    USB UAC                    USB Vendor            │
└─────────────────────────┼────────────────────────┼──────────────────┘
                          │ 24kHz PCM              │ JPEG/RGB565
                   ┌──────▼──────┐          ┌──────▼──────┐
                   │  ESP32-P4   │          │  ESP32-P4   │
                   │  (UAC)      │          │  (Display)  │
                   │  ES8388     │          │  800×480    │
                   │  MIC/SPK    │          │  RGB LCD    │
                   └─────────────┘          └─────────────┘
```

---

## 2. 硬件配置

### 2.1 ESP32-P4 引脚分配

| 功能 | GPIO | 说明 |
|------|------|------|
| **LCD_DATA[0:5]** | GPIO3-8 | RGB 数据 (B通道) |
| **LCD_DATA[6:7]** | GPIO13-14 | RGB 数据 (G通道低2位) |
| **LCD_DATA[8:11]** | GPIO15-18 | RGB 数据 (G通道高4位 + R通道低2位) |
| **LCD_DATA[12:15]** | GPIO19-22 | RGB 数据 (R通道高4位) |
| **LCD_CLK** | GPIO20 | 像素时钟 PCLK |
| **LCD_DE** | GPIO23 | 数据使能 |
| **LCD_HSYNC** | GPIO21 | 行同步 |
| **LCD_VSYNC** | GPIO2 | 帧同步 |
| **LCD_RST** | GPIO52 | 复位 |
| **LCD_BL** | GPIO53 | 背光控制 |
| **I2C_SDA** | GPIO33 | ES8388 / XL9555 |
| **I2C_SCL** | GPIO32 | ES8388 / XL9555 |
| **I2S_BCK** | GPIO47 | ES8388 SCLK |
| **I2S_WS** | GPIO48 | ES8388 LRCK |
| **I2S_DO** | GPIO49 | ES8388 SDIN (输出) |
| **I2S_DI** | GPIO50 | ES8388 SDOUT (输入) |
| **I2S_MCK** | GPIO46 | ES8388 MCLK |
| **XL9555_INT** | GPIO36 | IO 扩展中断 |

### 2.2 外设地址

| 器件 | 地址 | 用途 |
|------|------|------|
| ES8388 | 0x10 | 音频编解码 |
| XL9555 | 0x24 | GPIO 扩展 |

---

## 3. 固件功能状态

| 模块 | 状态 | 说明 |
|------|------|------|
| **USB UAC 播放** | ✅ 已完成 | 24kHz 16bit 单声道 PCM → ES8388 DAC |
| **USB UAC 录音** | ✅ 已完成 | ES8388 ADC → 24kHz 16bit PCM 上传 |
| **RGB LCD 显示** | ✅ 已完成 | 800×480 @ 60Hz，支持 JPEG/RGB565 |
| **USB Vendor 视频** | ✅ 已完成 | "UDSP" 帧协议，JPEG 压缩传输 |
| **USB HID** | ⚠️ 已实现但禁用 | 触控功能未启用 |
| **Wi-Fi** | ❌ 待实现 | STA 模式连接局域网 |

---

## 4. USB 通信协议

### 4.1 USB 配置

| 参数 | 值 |
|------|-----|
| **VID** | 0x303A |
| **PID** | 0x2986 |
| **速度** | USB 2.0 High Speed (480 Mbps) |
| **接口** | 复合设备: Vendor + Audio + HID |

### 4.2 UAC 音频格式

| 参数 | 值 |
|------|-----|
| **采样率** | 24000 Hz |
| **位深** | 16-bit |
| **声道** | 1 (单声道) |
| **端点** | EP4 OUT (播放), EP5 IN (录音) |
| **帧大小** | 480 bytes (10ms @ 24kHz) |

### 4.3 Vendor 显示协议

```
帧头 (16 字节):
+00: char magic[4]   = "UDSP"
+04: uint16_t type   = 0:JPEG, 1:RGB565
+06: uint16_t width
+08: uint16_t height
+10: uint32_t len    = payload 长度
+14: uint32_t frame_id

payload: 紧跟帧头的数据
```

---

## 5. 开发阶段

### 阶段 1: 环境搭建

#### 1.1 安装 ESP-IDF

```bash
# 设置 IDF 环境
export IDF_PATH=/home/nini/esp/esp-idf
source $IDF_PATH/export.sh

# 进入项目目录
cd /home/nini/airi_esp32p4/4.3/usb_800x480_RGBLCD
```

#### 1.2 配置目标芯片

```bash
idf.py set-target esp32p4
```

#### 1.3 构建固件

```bash
idf.py build
```

#### 1.4 烧录固件

```bash
idf.py -p /dev/ttyUSB0 flash monitor
```

### 阶段 2: 基础功能验证

#### 2.1 检查 USB 枚举

```bash
lsusb
# 应显示: Bus 001 Device xxx: ID 303a:2986

# Linux 下查看详细
lsusb -v -d 303a:2986
```

#### 2.2 ALSA 设备测试

```bash
# 查看音频设备
arecord -l   # 录音设备
aplay -l     # 播放设备

# 假设 ESP32-P4 是 card 2
# 录音测试 (10 秒)
arecord -D hw:2,0 -f S16_LE -r 24000 -c 1 -d 10 test.wav

# 播放测试
aplay -D hw:2,0 -f S16_LE -r 24000 -c 1 test.wav
```

#### 2.3 LCD 显示测试

```bash
# 使用正点原子提供的测试工具或 Python 脚本
python3 screen_stream_portal.py --test-frame --device /dev/ttyUSB0
```

### 阶段 3: AIRI USB 通信模块

#### 3.1 新增模块结构

```
packages/stage-usb/           # 新增 USB 通信包
├── src/
│   ├── index.ts              # 模块入口
│   ├── usb-device.ts         # USB 设备连接管理
│   ├── audio-stream.ts       # 音频流处理
│   ├── display-stream.ts     # 视频帧传输
│   └── protocol.ts           # 帧协议定义
├── package.json
└── tsconfig.json
```

#### 3.2 USB 设备连接

```typescript
// packages/stage-usb/src/usb-device.ts
import { connect, HID } from 'node-usb';

export class AiriUsbDevice {
  private device: HID;

  async connect() {
    // 连接 ESP32-P4
    this.device = await connect({
      deviceClass: 0xFF,  // Vendor Specific
      deviceSubclass: 0x00,
      protocol: 0x00,
    });

    // 设置接口
    await this.device.open();
    await this.device.claimInterface(0);
  }

  // 发送音频帧
  async sendAudioFrame(pcm: Buffer) {
    // UDSP 音频帧协议
    const frame = Buffer.alloc(16 + pcm.length);
    frame.write('AUD1', 0, 4, 'ascii');  // magic
    frame.writeUInt16LE(0, 4);            // seq
    frame.writeUInt16LE(pcm.length, 6);  // len
    pcm.copy(frame, 16);
    await this.device.write(1, frame);    // EP1 OUT
  }

  // 接收视频帧
  onVideoFrame(callback: (data: Buffer) => void) {
    this.device.on('data', (data) => {
      if (data.toString('ascii', 0, 4) === 'UDSP') {
        callback(data.slice(16));
      }
    });
  }
}
```

#### 3.3 修改 stage-tamagotchi

```typescript
// apps/stage-tamagotchi/src/main/services/usb-device.ts
import { AiriUsbDevice } from '@airi/stage-usb';

export class AiriUsbService {
  private device: AiriUsbDevice;

  async init() {
    this.device = new AiriUsbDevice();
    await this.device.connect();

    // 麦克风音频上传到 STT
    this.device.onAudioFrame((frame) => {
      this.hearingStore.feedAudio(frame);
    });
  }

  // 播放 TTS 音频
  async playTTS(pcmData: Buffer) {
    await this.device.sendAudioFrame(pcmData);
  }
}
```

### 阶段 4: 音频通路

#### 4.1 播放通路 (TTS → ESP32)

```
AIRI TTS (Kokoro/Whisper) → PCM 24kHz → USB Vendor Bulk → ESP32 → ES8388 DAC → Speaker
```

**ESP32 侧修改** (`main/APP/app_vendor.c`):
- 添加 Vendor Audio 端点接收
- PCM 数据写入 I2S DMA 环形缓冲区

#### 4.2 录音通路 (ESP32 → STT)

```
MIC → ES8388 ADC → I2S → ESP32 → USB Vendor Bulk → PC → STT (Whisper/DeepSeek)
```

**ESP32 侧修改**:
- I2S DMA 采集麦克风数据
- 通过 Vendor 端点上传 PCM

### 阶段 5: 显示通路

#### 5.1 视频帧传输

```
AIRI WebGL Canvas → JPEG 压缩 → USB Vendor Bulk → ESP32 → LCD 显示
```

**现有能力**:
- `app_vendor.c` 已实现 "UDSP" 帧协议
- `app_lcd.c` 支持 JPEG 解码显示

**待优化**:
- 帧率从 15fps 提升到 30fps
- BGR565 格式支持

---

## 6. 关键技术参数

### 6.1 音频延迟目标

| 阶段 | 延迟 | 说明 |
|------|------|------|
| USB 传输 | ~5ms | 480Mbps HS |
| I2S DMA | ~10ms | 10ms 缓冲 |
| ES8388 DAC | ~10ms | 转换延迟 |
| **总计** | **< 50ms** | 目标 |

### 6.2 显示帧率目标

| 参数 | 当前 | 目标 |
|------|------|------|
| 帧率 | 15 fps | 30 fps |
| 分辨率 | 800×480 | 800×480 |
| 格式 | JPEG | JPEG |

### 6.3 USB 带宽估算

```
音频: 24kHz × 16bit × 1ch = 48 KB/s ≈ 384 Kbps
视频: 30fps × 50KB/帧 (JPEG) ≈ 1.5 MB/s ≈ 12 Mbps
总计: ~13 Mbps << 480 Mbps (USB HS 上限)
```

---

## 7. 文件索引

### 7.1 ESP32 固件关键文件

| 文件 | 功能 |
|------|------|
| `main/main.c` | 应用入口 |
| `main/APP/app_usb.c` | USB 总线初始化 |
| `main/APP/app_uac.c` | UAC 音频处理 |
| `main/APP/app_vendor.c` | Vendor 显示数据 |
| `main/APP/app_lcd.c` | LCD 显示控制 |
| `main/UAC/usb_device_uac.c` | UAC 设备驱动 |
| `components/BSP/ES8388/es8388.c` | ES8388 驱动 |
| `components/BSP/LCD/rgblcd.c` | RGB LCD 驱动 |

### 7.2 AIRI 关键文件

| 文件 | 功能 |
|------|------|
| `packages/stage-ui/src/stores/hearing.ts` | STT 语音识别 |
| `packages/stage-ui/src/stores/llm.ts` | LLM 对话 |
| `packages/stage-ui/src/utils/tts.ts` | TTS 语音合成 |
| `packages/stage-ui-three/` | 3D 渲染引擎 |
| `apps/stage-tamagotchi/` | Electron 主应用 |

---

## 8. 验证清单

### 固件验证

- [ ] USB 枚举成功，lsusb 显示正确 PID/VID
- [ ] ALSA 能识别 UAC 设备
- [ ] 录音和播放功能正常
- [ ] LCD 显示测试图案正常

### AIRI 集成验证

- [ ] USB 设备能被 Electron/navigator.hid 识别
- [ ] TTS 音频能通过 USB 播放
- [ ] 麦克风音频能上传到 STT
- [ ] 数字人画面能显示在 LCD 上

### 端到端验证

- [ ] 语音对话完整流程
- [ ] 延迟可接受 (< 500ms)
- [ ] 长时间运行稳定

---

## 9. 开发时间估算

| 阶段 | 内容 | 预估 |
|------|------|------|
| 1 | 环境搭建 | 1 天 |
| 2 | 基础功能验证 | 1 天 |
| 3 | AIRI USB 通信模块 | 1 周 |
| 4 | 音频通路集成 | 1 周 |
| 5 | 显示通路集成 | 1 周 |
| 6 | 端到端调试 | 1 周 |
| **总计** | | **5-6 周** |

---

## 10. 已知问题与风险

| 问题 | 影响 | 应对 |
|------|------|------|
| USB Vendor 驱动 | Windows 需要安装驱动 | 提供 WinUSB inf 文件 |
| Linux PipeWire | 音频路由复杂 | 配置 udev 规则 |
| BGR565 颜色顺序 | LCD 颜色偏色 | 修改固件或转换格式 |
| 音频延迟 | 影响交互体验 | 优化缓冲策略 |
