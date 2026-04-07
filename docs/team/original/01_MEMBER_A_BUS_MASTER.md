# 成员A 工作内容与流程文档

## 基本信息

| 项目 | 内容 |
|------|------|
| **代号** | 总线大师 (Bus Master) |
| **角色** | 项目架构师 & USB协议栈负责人 |
| **技术领域** | USB协议、TinyUSB框架、FreeRTOS系统集成 |

---

## 一、核心职责

### 1.1 USB协议栈管理
- USB PHY初始化和时钟配置
- TinyUSB框架集成和维护
- USB描述符管理和维护
- 系统集成和任务调度

### 1.2 Vendor模式实现
- 数据接收和帧解析
- CRC16校验（MODBUS多项式0xA001）
- 帧同步机制（sync marker "UDSP"）
- 512字节帧头解析

---

## 二、工作流程

### 2.1 系统初始化流程

```
app_main()
│
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

### 2.2 Vendor数据接收流程

```
tud_vendor_rx_cb()
│
├── tud_vendor_n_available()  # 检查接收数据
├── tud_vendor_n_read()       # 读取数据
├── Search "UDSP" sync marker  # 搜索同步标记
├── Validate CRC16             # CRC校验
├── Parse frame header (512 bytes)  # 解析帧头
├── Check dimension match (800x480) # 尺寸校验
└── buffer_fill()
    ├── frame_add_data()
    └── frame_send_filled()
```

### 2.3 USB描述符配置

| 描述符类型 | 配置值 |
|-----------|--------|
| VID | 0x303A |
| PID | 0x2986 |
| USB速度 | HS (480Mbps) |
| 配置数量 | 1 |
| 接口数量 | 3 (Vendor + UAC + HID) |

---

## 三、关键代码模块

| 文件 | 功能 |
|------|------|
| `main/APP/app_usb.c` | USB设备栈管理 |
| `main/APP/app_vendor.c` | Vendor自定义设备类 |
| `main/APP/usb_descriptors.c` | USB描述符定义 |
| `main/APP/tusb_config.h` | TinyUSB配置 |
| `main/main.c` | 程序入口、系统初始化 |
| `main/APP/app_config.h` | 应用配置参数 |

---

## 四、预期挑战与解决方案

### 挑战1：USB连接不稳定或断开

**问题描述**：
- USB枚举失败或频繁断开
- LIBUSB_ERROR_ACCESS权限问题
- 设备无法被PC识别

**解决方案**：
```bash
# 创建udev规则解决权限问题
# /etc/udev/rules.d/99-esp32-p4-display.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="303a", ATTR{idProduct}=="2986", MODE="0666"
```
- 检查USB PHY时钟配置是否正确
- 确认GPIO引脚复用配置（USB D+/D-使用专用引脚）
- 验证描述符VID/PID与PC驱动匹配

### 挑战2：Vendor数据丢帧

**问题描述**：
- 数据接收不完整
- CRC校验失败
- 帧同步丢失

**解决方案**：
- 实现双缓冲机制避免数据覆盖
- 增加超时检测和重同步机制
- 优化"UDSP"标记搜索算法
- 验证CRC16实现（多项式0xA001）

### 挑战3：高帧率传输性能瓶颈

**问题描述**：
- 帧率无法达到30fps以上
- 数据传输延迟过高

**解决方案**：
- 使用DMA传输减少CPU占用
- 调整USB批量传输大小
- 优化帧缓冲管理（当前8个缓冲区）
- 考虑JPEG压缩减少数据量

### 挑战4：多任务调度冲突

**问题描述**：
- USB中断与其他任务冲突
- FreeRTOS任务优先级配置问题

**解决方案**：
- USB设备任务使用高优先级
- 使用队列进行任务间通信
- 合理配置栈空间和堆内存
- 使用互斥量保护共享资源

---

## 五、调试方法

### 5.1 串口日志输出
```
I (856) app_usb: USB Mount
I (860) app_usb: USB Device Stack Init Success
```

### 5.2 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 设备未识别 | VID/PID不匹配 | 检查usb_descriptors.c配置 |
| 传输丢包 | 缓冲区不足 | 增加帧缓冲数量 |
| CRC错误 | 数据损坏 | 检查USB线材质量 |
| 帧撕裂 | 同步问题 | 检查帧发送时序 |

### 5.3 测试命令
```bash
# 发送RGB565测试帧
npx tsx apps/stage-tamagotchi/scripts/test-usb-display.ts --test-frame --vid=0x303a --pid=0x2986
```

---

## 六、交接检查清单

### 6.1 代码质量
- [ ] USB初始化流程完整
- [ ] Vendor数据接收稳定
- [ ] CRC校验正确
- [ ] 帧同步机制可靠

### 6.2 文档更新
- [ ] USB协议规范已更新
- [ ] 描述符配置已记录
- [ ] 调试方法已完善

---

> **文档版本**: V1.0
> **创建日期**: 2026-04-02
> **维护人**: 成员A (总线大师)
