# ESP32-P4 UAC 音频开发总结

## 1. 项目概述

**目标**: 在 Ubuntu 系统上实现 ESP32-P4 开发板的 USB Audio Class 2 (UAC2) 音频功能
- PC → 设备: 音频播放 (通过 ES8388 codec 输出)
- 设备 → PC: 音频录音 (通过 ES8388 MIC 输入)
- 音频参数: 24kHz 采样率, 16位位宽, 单声道

**硬件平台**: 正点原子 ESP32-P4 开发板 + ES8388 音频编解码器

## 2. 音频参数配置

| 参数 | 值 |
|------|-----|
| 采样率 | 24000 Hz |
| 位宽 | 16 bit |
| 通道数 | 1 (单声道) |
| 帧大小 | 480 bytes (10ms × 24000Hz × 1ch × 2bytes) |

## 3. 关键文件

### 3.1 配置文件

- [main/UAC/uac_config.h](main/UAC/uac_config.h) - UAC 参数定义
- [main/UAC/tusb_config_uac.h](main/UAC/tusb_config_uac.h) - TinyUSB UAC 配置
- [main/APP/tusb_config.h](main/APP/tusb_config.h) - TinyUSB 通用配置

### 3.2 业务逻辑

- [main/UAC/usb_device_uac.c](main/UAC/usb_device_uac.c) - UAC 设备驱动
- [main/APP/app_uac.c](main/APP/app_uac.c) - UAC 应用层 (回调函数)
- [main/APP/usb_descriptors.c](main/APP/usb_descriptors.c) - USB 描述符

### 3.3 底层驱动

- `components/BSP/ES8388/es8388.c` - ES8388 codec 驱动
- `components/BSP/MYI2S/myi2s.c` - I2S 接口驱动

## 4. 主要修改

### 4.1 配置描述符 (usb_descriptors.c:97-99)

```c
#define CONFIG_TOTAL_LEN    (TUD_CONFIG_DESC_LEN + VENDOR_DESC_TOTAL_LEN + \
                             TUD_HID_DESC_LEN * CFG_TUD_HID + \
                             CFG_TUD_AUDIO_FUNC_1_DESC_LEN * CFG_TUD_AUDIO)
```

### 4.2 禁用反馈端点 (tusb_config_uac.h:23)

```c
#define CFG_TUD_AUDIO_ENABLE_FEEDBACK_EP    0
```

### 4.3 反馈回调保护 (usb_device_uac.c)

```c
#if CFG_TUD_AUDIO_ENABLE_FEEDBACK_EP
void tud_audio_feedback_params_cb(...) { ... }
#endif
```

### 4.4 UAC 应用层回调 (app_uac.c)

| 回调函数 | 功能 |
|----------|------|
| `uac_output_cb()` | PC→设备音频数据，写入 I2S TX |
| `uac_input_cb()` | 设备→PC音频数据，从 I2S RX 读取 |
| `uac_set_mute_cb()` | 静音控制 |
| `uac_set_volume_cb()` | 音量控制 (0-100 → 0-33) |

## 5. 问题排查记录

### 5.1 TUD_AUDIO_DESC_LEN 未声明

- **原因**: 宏名称错误
- **解决**: 改用 `CFG_TUD_AUDIO_FUNC_1_DESC_LEN`

### 5.2 dcd_edpt_close 崩溃

- **原因**: 关闭反馈等时端点时 DWC2 驱动异常
- **解决**: 禁用 `CFG_TUD_AUDIO_ENABLE_FEEDBACK_EP`

### 5.3 audio_feedback_params_t 未声明

- **原因**: 禁用反馈后回调函数仍被引用
- **解决**: 用 `#if CFG_TUD_AUDIO_ENABLE_FEEDBACK_EP` 包裹回调

### 5.4 PulseAudio 不显示设备

- **原因**: PipeWire/PulseAudio 兼容性问题
- **解决**: ALSA 直接访问可用，无需修复

## 6. 验证结果

### 6.1 设备枚举

```
Bus 001 Device 002: ID 303a:2986 Espressif USB Audio
```

### 6.2 ALSA 设备

```
Card 2: DNESP32P4 [DNESP32P4], device 0: UAC1 [UAC1_GUITAR]
```

### 6.3 测试命令

**录音**:
```bash
arecord -D hw:2,0 -f S16_LE -r 24000 -c 1 test.wav
```

**播放**:
```bash
aplay -D hw:2,0 -f S16_LE -r 24000 -c 1 test.wav
```

### 6.4 lsusb 端点信息

| 端点 | 方向 | 类型 | 用途 |
|------|------|------|------|
| EP4 OUT | PC→设备 | 等时 | 扬声器 |
| EP5 IN | 设备→PC | 等时 | 麦克风 |
| EP6 IN | 设备→PC | 等时 | 反馈(未启用) |

## 7. 后续扩展

- 音视频同步传输 (视频走 Vendor Bulk + 音频走 UAC)
- 提高采样率 (当前 24kHz)
- PulseAudio 集成测试
