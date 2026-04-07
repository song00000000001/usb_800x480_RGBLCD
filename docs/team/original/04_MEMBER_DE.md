# 成员DE 工作内容与流程文档

## 基本信息

| 项目 | 内容 |
|------|------|
| **代号** | 声波捕手 + 端点使者 (Sound Catcher + Endpoint Envoy) |
| **角色** | 音频子系统 + PC端开发负责人 |
| **技术领域** | USB Audio Class (UAC)、ES8388音频Codec、I2S音频接口、Electron/Node.js、USB通信、WebGL、TypeScript/Vue |

---

## 一、核心职责

### 1.1 UAC音频设备驱动
- USB Audio Class设备驱动开发
- 双向音频流管理（播放+录音）
- 音量/静音控制
- 采样率配置

### 1.2 音频Codec集成
- ES8388配置和控制
- I2S音频接口对接
- 音频数据路由

### 1.3 AIRI Electron App开发
- USB显示服务集成
- WebGL canvas帧捕获
- USB协议通信实现
- IPC通信封装

### 1.4 PC端功能扩展
- USB设备连接管理
- 帧数据发送
- 协议解析和封装

---

## 二、工作流程

### 2.1 UAC系统初始化

```
app_uac_init()
│
├── es8388_init()              # ES8388音频Codec初始化
├── myi2s_init()               # I2S接口初始化
├── uac_register_callbacks()   # 注册音量/静音回调
└── 创建音频任务
    ├── uac_playback_task()    # 播放任务
    └── uac_capture_task()     # 录音任务
```

### 2.2 音频播放流程

```
PC (UAC Audio) → USB IN Endpoint → tud_audio_n_received_cb()
    │
    └── app_uac Speaker Callback
        │
        └── myi2s_write() → I2S → ES8388 → 喇叭输出
```

### 2.3 音频录制流程

```
麦克风输入 → ES8388 → I2S → myi2s_read()
    │
    └── app_uac Mic Callback
        │
        └── tud_audio_n_transmit() → USB OUT Endpoint → PC
```

### 2.4 USB显示服务架构

```
┌─────────────────────────────────────────────────────────┐
│                    AIRI Electron App                     │
├─────────────────────────────────────────────────────────┤
│  Vue Component (UsbDisplayToggle.vue)                   │
│      │                                                  │
│      ▼                                                  │
│  use-usb-display.ts (IPC Wrapper)                       │
│      │                                                  │
│      ▼                                                  │
│  usb-display/index.ts (USB Service)                     │
│      │                                                  │
│      ▼                                                  │
│  use-usb-display-stream.ts (Stream Composable)           │
│      │                                                  │
│      ▼                                                  │
│  frame-capture.ts (WebGL Canvas)                        │
└─────────────────────────────────────────────────────────┘
                          │
                          │ USB (libusb/native USB)
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    ESP32-P4 Device                       │
│  Vendor Endpoint (0x01 OUT)                             │
└─────────────────────────────────────────────────────────┘
```

### 2.5 帧发送流程

```
frame-capture.ts
│
├── WebGL canvas读取像素
├── 转换为BGR565格式
└── 传递给usb-display服务

usb-display/index.ts
│
├── 创建USB设备连接 (VID=0x303A, PID=0x2986)
├── 构建512字节帧头
│   ├── sync = "UDSP"
│   ├── crc16 = MODBUS CRC16
│   ├── type = 3 (JPEG)
│   ├── width = 800, height = 480
│   └── frame_id
└── 批量传输到Endpoint 0x01
```

---

## 三、关键代码模块

### 音频部分

| 文件 | 功能 |
|------|------|
| `main/UAC/usb_device_uac.c` | UAC设备驱动核心 |
| `main/UAC/uac_config.h` | UAC配置参数 |
| `main/UAC/tusb_config_uac.h` | TinyUSB UAC配置 |
| `main/UAC/uac_descriptors.h` | UAC描述符 |
| `main/APP/app_uac.c` | UAC应用层 |
| `components/BSP/ES8388/es8388.c` | ES8388 Codec驱动 |

### PC端部分

| 文件路径 | 功能 |
|----------|------|
| `frame-capture.ts` | WebGL canvas帧捕获，BGR565支持 |
| `use-usb-display-stream.ts` | AIRI视频流composable |
| `use-usb-display.ts` | Renderer IPC封装 |
| `usb-display/index.ts` | USB显示服务，协议实现 |
| `UsbDisplayToggle.vue` | USB显示UI开关组件 |
| `test-usb-display.ts` | RGB565测试脚本 |

---

## 四、音频参数配置

| 参数 | 配置值 |
|------|--------|
| 采样率 | 24kHz |
| 位深 | 16位 |
| 声道 | 单声道 (Mono) |
| 传输方向 | 双向 (Speaker + Mic) |

### 4.1 UAC描述符配置
```c
// 采样率描述
static const uint32_t sample_rate[] = {24000};

// 通道配置
#define TUSB_TUD_AUDIO_FUNC_1_N_BYTES_PER_SAMPLE_IS_2 (1)  // 16位
#define TUSB_TUD_AUDIO_FUNC_1_N_CHANNELS_TX (1)           // 1通道
#define TUSB_TUD_AUDIO_FUNC_1_N_CHANNELS_RX (1)           // 1通道
```

---

## 五、ES8388寄存器配置

### 5.1 关键寄存器
```c
#define ES8388_ADDR 0x10

// 初始化序列
ES8388_CHIPIP = 0x00;        // 唤醒Codec
ES8388_CONTROL1 = 0x00;      // 正常模式
ES8388_DACCONTROL1 = 0x18;   // 16位I2S
ES8388_DACCONTROL2 = 0x02;   // 48kHz（虽然UAC用24kHz）
ES8388_ADCCONTROL1 = 0x44;   // 24kHz采样
ES8388_ADCCONTROL2 = 0x00;   // 单声道麦克风
```

### 5.2 音频路由
```
播放: I2SDOUT → DAC → Headphone/Lineout
录音: Mic/Linein → ADC → I2SDIN
```

---

## 六、USB协议实现

### 6.1 帧头格式（512字节）
```typescript
interface FrameHeader {
  sync: Buffer;        // "UDSP" (4 bytes)
  crc16: number;        // MODBUS CRC16 (2 bytes)
  type: number;         // 0=RGB565, 1=RGB888, 2=YUV420, 3=JPEG
  cmd: number;          // 命令 (1 byte)
  x: number;            // X偏移 (2 bytes)
  y: number;            // Y偏移 (2 bytes)
  width: number;        // 帧宽度 (2 bytes)
  height: number;       // 帧高度 (2 bytes)
  frame_info: number;   // frame_id | (payload_total << 10)
}
```

### 6.2 CRC16实现
```typescript
function calculateCRC16(data: Buffer): number {
  let crc = 0xFFFF;
  for (const byte of data) {
    crc ^= byte;
    for (let j = 0; j < 8; j++) {
      if (crc & 1) {
        crc = (crc >> 1) ^ 0xA001;
      } else {
        crc >>= 1;
      }
    }
  }
  return crc;
}
```

### 6.3 像素格式转换
```typescript
// RGB转BGR565（ESP32-P4固件期望BGR565）
function rgbToBGR565(r: number, g: number, b: number): number {
  const b5 = (b >> 3) & 0x1F;
  const g6 = (g >> 2) & 0x3F;
  const r5 = (r >> 3) & 0x1F;
  return (b5 << 11) | (g6 << 5) | r5;
}
```

---

## 七、VID/PID配置

| 参数 | 值 | 说明 |
|------|-----|------|
| VID | 0x303A | Espressif USB Vendor ID |
| PID | 0x2986 | 设备Product ID |
| 接口数 | 3 | Vendor + UAC + HID |

---

## 八、预期挑战与解决方案

### 挑战1：USB音频传输延迟高

**问题描述**：
- 音频播放有延迟
- 录音和播放不同步

**解决方案**：
- 优化USB音频缓冲区大小（不宜过大）
- 调整FreeRTOS任务优先级
- 使用零拷贝数据传输
- 配置合理的采样率（24kHz已优化）

### 挑战2：ES8388初始化失败

**问题描述**：
- 音频无声
- I2C通信错误

**解决方案**：
```c
// 检查ES8388 I2C地址（0x10）
// 确认I2C通信正常后再配置ES8388
esp_err_t ret = es8388_init();
if (ret != ESP_OK) {
    ESP_LOGE("UAC", "ES8388 init failed: %s", esp_err_to_name(ret));
    return ret;
}
```
- 检查ES8388供电
- 验证I2C总线连接
- 检查ES8388 RESET引脚

### 挑战3：音频噪声或失真

**问题描述**：
- 播放有杂音
- 录音失真
- 爆音

**解决方案**：
- 检查ES8388的I2S格式配置（MSB Justified）
- 确认MCLK频率正确（24kHz * 256 = 6.144MHz）
- 检查ES8388的ADC/DAC增益设置
- 验证电源噪声滤除

### 挑战4：音量控制无效

**问题描述**：
- 音量调节无效果
- 静音功能不工作

**解决方案**：
```c
// 注册音量回调
tud_audio_set_itf_cb(APP_UAC_AUDIO_INTERFACE, &audio_callbacks);

// 回调函数中处理音量
bool tud_audio_set_volume_cb(uint8_t volume) {
    es8388_set_volume(volume);  // 0-100
    return true;
}
```
- 检查音量回调是否正确注册
- 验证ES8388音量寄存器映射
- 确认PC端音量同步

### 挑战5：LIBUSB_ERROR_ACCESS权限问题

**问题描述**：
- USB设备无法打开
- 权限被拒绝

**解决方案**：
```bash
# Linux: 创建udev规则
# /etc/udev/rules.d/99-esp32-p4-display.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="303a", ATTR{idProduct}=="2986", MODE="0666"

# 重新加载规则
sudo udevadm control --reload-rules
sudo udevadm trigger
```
- Windows: 以管理员身份运行
- macOS: 检查系统偏好设置中的安全许可

### 挑战6：颜色显示错误（红蓝互换）

**问题描述**：
- 颜色显示偏红/偏蓝
- 图像颜色异常

**原因**：固件期望BGR565格式，但发送的是RGB565

**解决方案**：
```typescript
// 正确转换RGB为BGR
const bgr565 = (r5 << 11) | (g6 << 5) | b5;  // 错误！
const bgr565 = (b5 << 11) | (g6 << 5) | r5;  // 正确！
```
- 确保frame-capture.ts中的像素格式转换正确
- 检查usb-display/index.ts中的颜色通道顺序

### 挑战7：帧率低或卡顿

**问题描述**：
- 帧率无法达到15fps以上
- 画面卡顿不流畅

**解决方案**：
- 使用JPEG压缩减少数据量（推荐）
- 优化WebGL canvas读取性能
- 使用Transferable对象减少内存复制
- 批量传输大块数据
- 增加USB传输缓冲区

### 挑战8：USB设备断开重连

**问题描述**：
- 设备意外断开
- 重连后无法恢复

**解决方案**：
```typescript
// 监听设备断开事件
device.addEventListener('disconnect', async () => {
  await handleDeviceDisconnect();
});

// 实现重连逻辑
async function handleDeviceDisconnect() {
  // 清理资源
  await closeDevice();
  // 等待设备重新插入
  await waitForDevice();
  // 重新初始化
  await openDevice();
}
```

### 挑战9：JPEG压缩质量与速度平衡

**问题描述**：
- JPEG压缩太慢
- JPEG文件太大

**解决方案**：
- 调整JPEG质量参数（70-85%为平衡点）
- 使用硬件加速编码（如果浏览器支持）
- 考虑使用WebAssembly JPEG编码器
- 预压缩策略：每隔几帧传输一次JPEG

---

## 九、调试方法

### 9.1 串口日志（音频）
```
I (xxx) app_uac: UAC initialized
I (xxx) app_uac: Speaker sample rate: 24000 Hz
I (xxx) app_uac: Mic sample rate: 24000 Hz
```

### 9.2 音频测试
```bash
# Linux播放测试
aplay -D hw:1 -r 24000 -f S16_LE test.wav

# 录音测试
arecord -D hw:1 -r 24000 -f S16_LE test.wav
```

### 9.3 I2S时钟检查
- 使用示波器测量GPIO50 (MCLK)：应为6.144MHz
- 测量GPIO49 (BCK)：应为1.536MHz (24kHz * 64)
- 测量GPIO48 (WS)：应为24kHz

### 9.4 PC端测试命令
```bash
# RGB565测试帧
npx tsx apps/stage-tamagotchi/scripts/test-usb-display.ts --test-frame --vid=0x303a --pid=0x2986

# Python JPEG发送
python3 apps/stage-tamagotchi/scripts/send_usb_frame.py 0x303a 0x2986 800 480 0 "255,0,0" jpeg
```

### 9.5 WebGL帧捕获测试
```typescript
import { captureFrame } from '@/composables/frame-capture';

const frame = await captureFrame(canvas);
console.log(`Frame captured: ${frame.width}x${frame.height}, ${frame.data.length} bytes`);
```

---

## 十、GPIO资源

| GPIO | 功能 | 说明 |
|------|------|------|
| GPIO46 | I2S_SDOUT | 音频数据输出 |
| GPIO47 | I2S_SDIN | 音频数据输入 |
| GPIO48 | I2S_WS | 字选择 |
| GPIO49 | I2S_BCK | 位时钟 |
| GPIO50 | I2S_MCLK | 主时钟 |

---

## 十一、交接检查清单

### 11.1 功能验证
- [ ] UAC设备枚举成功
- [ ] Speaker播放正常
- [ ] Mic录音正常
- [ ] 音量控制响应
- [ ] USB设备连接成功
- [ ] 帧发送正常
- [ ] 颜色显示正确

### 11.2 性能指标
- [ ] 采样率稳定24kHz
- [ ] 延迟<50ms
- [ ] 无明显噪声
- [ ] 帧率>=15fps
- [ ] 显示延迟<100ms

### 11.3 文档更新
- [ ] UAC配置参数已记录
- [ ] ES8388初始化序列已记录
- [ ] USB协议实现已记录
- [ ] 测试命令已更新
- [ ] 常见问题已记录

---

> **文档版本**: V1.0
> **创建日期**: 2026-04-02
> **合并维护人**: 成员DE (声波捕手 + 端点使者)
