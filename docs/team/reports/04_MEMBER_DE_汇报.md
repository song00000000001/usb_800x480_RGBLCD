# 工作汇报

## 成员DE（声波捕手 + 端点使者）— 音频子系统与PC端开发

### 一、项目背景与职责概述

本项目包含两个核心子系统：音频子系统和PC端显示服务。音频子系统通过USB Audio Class（UAC）实现免驱音频设备，支持播放和录音功能；PC端应用通过Electron/Node.js技术栈开发，负责WebGL帧捕获和USB协议通信，将屏幕内容实时传输到ESP32-P4设备显示。

作为合并后的负责人，我同时承担UAC设备驱动开发、ES8388音频Codec集成、以及AIRI Electron应用的完整实现工作。

### 二、具体工作内容

#### 音频子系统

**UAC设备驱动开发**

USB Audio Class是USB标准类之一，PC操作系统自带驱动，插入设备后即可自动识别使用。我基于TinyUSB框架实现了UAC功能，支持以下特性：双向音频流（播放+录音）、音量控制和静音功能、可配置采样率。

UAC描述符配置是关键。采样率数组定义为{24000}Hz，支持24kHz采样。通道配置为单声道（MONO），位深为16位。TX和RX通道数都配置为1。

UAC初始化流程为：es8388_init() → myi2s_init() → uac_register_callbacks() → 创建音频任务。音频任务分为播放任务（uac_playback_task）和录音任务（uac_capture_task），分别处理音频的输出和输入。

**音频播放流程**

当PC端发送音频数据时，数据通过USB IN端点到达设备。TinyUSB调用tud_audio_n_received_cb()回调函数，我在这个回调中将接收到的音频数据写入I2S接口：tud_audio_n_received_cb() → myi2s_write() → I2S总线 → ES8388 DAC → 喇叭输出。

整个链路需要保证时序精确。I2S数据格式为标准I2S_phillips，左对齐，MSB先出。ES8388接收到I2S数据后进行数模转换，输出到耳机或扬声器。

**音频录制流程**

录音方向是播放的逆过程：麦克风或Line输入 → ES8388 ADC → I2S → myi2s_read() → TinyUSB → USB OUT端点 → PC。

ES8388的ADC配置为单声道模式，采样率24kHz。I2S数据格式与播放一致，确保数据通路兼容。

**ES8388 Codec集成**

ES8388是一款高性能立体声音频Codec，支持I2S接口。我通过I2C接口配置其内部寄存器：唤醒Codec（CHIPIP = 0x00）、设置控制模式（CONTROL1 = 0x00）、配置DAC（16位I2S格式）、配置ADC（24kHz采样率）、设置输入输出增益等。

播放路由：I2SDOUT → DAC → Headphone/Lineout
录音路由：Mic/Linein → ADC → I2SDIN

#### PC端应用

**AIRI Electron应用架构**

AIRI是一个基于Electron的桌面应用，采用Vue作为UI框架，通过IPC机制连接渲染进程和主进程。USB显示功能的架构层次为：Vue组件（UsbDisplayToggle.vue）→ IPC封装（use-usb-display.ts）→ USB服务（usb-display/index.ts）→ StreamComposable（use-usb-display-stream.ts）→ 帧捕获（frame-capture.ts）。

用户通过UI开关控制USB显示功能，Vue组件发出指令后，经过层层封装，最终到达USB服务层执行实际的设备通信。

**WebGL Canvas帧捕获**

frame-capture.ts负责从WebGL canvas读取像素数据。这是实现屏幕内容捕获的关键步骤。捕获的像素数据最初是标准的RGB888格式，需要转换为设备期望的BGR565格式。

RGB到BGR565的转换公式为：提取红色5位（r>>3）、绿色6位（g>>2）、蓝色5位（b>>3），然后组合为(b5<<11) | (g6<<5) | r5。这个转换必须准确，否则显示颜色会出错。

**USB协议实现**

USB显示服务（usb-display/index.ts）是协议实现的核心。连接设备时，使用VID=0x303A、PID=0x2986创建设备实例。

发送显示帧时，需要构建完整的512字节帧头：sync字段为"UDSP"（4字节）、crc16为MODBUS CRC16校验值（2字节）、type标识数据类型（3表示JPEG）、cmd为命令字节、x/y为偏移坐标、width/height为分辨率、frame_info包含frame_id和payload长度信息。帧头之后是实际的数据负载，通过批量传输发送到Endpoint 0x01。

CRC16校验采用MODBUS标准，多项式为0xA001，与ESP32-P4端保持一致。

**协议解析与封装**

发送流程为：frame-capture.ts捕获canvas像素 → 转换为BGR565格式 → 传递给usb-display服务 → 构建帧头并计算CRC → 批量传输到设备。

设备通过Vendor Endpoint 0x01接收数据，每帧数据都包含同步标记和CRC校验，确保数据传输的可靠性。

### 三、遇到的挑战与解决方案

**USB音频传输延迟高**

播放音频时能明显感觉到延迟，录音和播放不同步。这严重影响用户体验，尤其是视频通话场景。

延迟的来源包括：USB音频缓冲区过大、数据在端点和应用之间拷贝过多、FreeRTOS任务调度不及时等。

我采取了以下优化措施：减小USB音频缓冲区大小（但不能过小导致断音）、使用零拷贝技术减少数据复制、调整FreeRTOS任务优先级确保音频任务及时执行、保持采样率为24kHz的稳定配置。

**ES8388初始化失败**

音频无声，首先怀疑ES8388初始化问题。I2C通信错误、寄存器配置不当都可能导致Codec无法正常工作。

我编写了详细的初始化检查代码，验证每一步的返回值：确认ES8388 I2C地址为0x10、检查I2C总线通信正常、验证I2C写入的每个寄存器值、确认RESET引脚状态正确。

发现主要失败原因是I2C通信不稳定，修复连接后问题解决。

**音频噪声和失真**

播放时出现杂音，录音时有滴答声，偶发爆音。这是音频系统常见的问题，来源多样。

我系统地排查了各个环节：验证ES8388的I2S格式配置为MSB Justified标准、检查MCLK频率是否为6.144MHz（24kHz × 256）、确认ADC/DAC增益设置在合理范围、检查电源噪声是否被引入模拟电路。

调整后音频质量显著改善。

**音量控制无效**

PC端调节音量没有效果，静音功能也不工作。这说明音量回调函数可能没有正确注册或调用。

我检查了TinyUSB的回调注册机制：确保tud_audio_set_itf_cb()正确注册音量回调、在回调函数中调用es8388_set_volume()设置Codec音量、验证音量值范围（0-100）与ES8388寄存器映射正确。

**LIBUSB_ERROR_ACCESS权限问题**

Linux下非root用户无法打开USB设备，LIBUSB_ERROR_ACCESS错误频繁出现。这是因为USB设备默认权限较为严格。

我通过创建udev规则解决：编写/etc/udev/rules.d/99-esp32-p4-display.rules文件，设置ATTR{idVendor}=="303a"和ATTR{idProduct}=="2986"的设备权限为MODE="0666"。修改规则后需要执行sudo udevadm control --reload-rules和sudo udevadm trigger重新加载。

Windows用户需要以管理员身份运行程序，macOS用户需要在系统偏好设置中授权。

**颜色显示错误（红蓝互换）**

开发过程中发现显示颜色偏红或偏蓝，与实际画面不符。排查发现是颜色格式转换错误。

ESP32-P4固件期望BGR565格式，但我的代码错误地按照RGB565发送。正确做法是在转换时交换颜色通道顺序：对于RGB输入，转换公式应为(b5<<11) | (g6<<5) | r5，而不是(r5<<11) | (g6<<5) | b5。修复后颜色显示正常。

**帧率低和卡顿**

帧率只有个位数，画面严重卡顿。用户无法接受这样的显示效果。

分析后发现瓶颈在于数据量过大和传输效率低下。800x480分辨率的RGB565数据量约为768KB，每帧都需要通过USB传输，带宽压力很大。

我采取了多项优化：推荐使用JPEG压缩（数据量可压缩到原来的10-20%）、优化WebGL canvas读取性能减少GPU开销、使用Transferable对象在worker间传递数据减少内存拷贝、批量传输大块数据减少协议开销、增加USB传输缓冲区提升吞吐效率。

**USB设备断开重连**

设备意外断开后，应用无法自动恢复连接，用户必须重新插拔USB线并重启应用。

我在代码中实现了断开监听和重连机制：device.addEventListener('disconnect', ...)监听断开事件，触发后执行handleDeviceDisconnect()清理资源并等待设备重新插入，重新插入后自动初始化设备。

**JPEG压缩质量与速度平衡**

JPEG压缩太慢会影响帧率，压缩质量太低又会影响画面清晰度。这是一个需要权衡的问题。

我通过大量测试确定了70-85%的质量范围作为平衡点。如果浏览器支持，可以考虑使用WebAssembly JPEG编码器提升压缩速度。还可以采用预压缩策略，每隔几帧传输一次完整JPEG，中间帧只传输差异部分。

### 四、工作成果

**音频子系统成果**

音频子系统目前运行稳定，具体成果包括：UAC设备被PC成功枚举为音频设备、支持Speaker播放和Mic录音双向功能、音量控制和静音功能正常工作、采样率稳定在24kHz、延迟控制在50ms以内、音频质量无明显噪声。

调试能力方面：串口日志输出UAC初始化信息和采样率、通过Linux的aplay/arecord工具可进行播放录音测试、I2S时钟可使用示波器验证（GPIO50 MCLK=6.144MHz、GPIO49 BCK=1.536MHz、GPIO48 WS=24kHz）。

**PC端应用成果**

PC端应用目前运行良好，具体成果包括：USB设备连接成功，被PC正确识别、帧发送功能正常，支持RGB565和JPEG两种格式、颜色显示正确，BGR565转换验证通过、帧率达到15fps以上、延迟控制在100ms以内、实现了完整的断开重连机制。

测试能力方面：提供了RGB565测试帧发送脚本（npx tsx test-usb-display.ts --test-frame）、支持Python JPEG发送脚本（python3 send_usb_frame.py）、WebGL帧捕获可独立测试验证。

### 五、总结与展望

音频子系统的开发让我深入理解了USB Audio Class标准和I2S音频接口的时序要求。PC端开发让我掌握了Electron下的USB设备通信技术，积累了丰富的协议实现经验。

未来计划：音频子系统优化延迟到30ms以下、增加对多种采样率的支持、探索回声消除和降噪功能以提升录音质量；PC端优化JPEG编码性能提升帧率、增加多显示器支持、实现屏幕局部更新以进一步优化带宽占用，并考虑开发配置工具让用户自定义分辨率和帧率参数。

---

> **汇报人**：成员DE（声波捕手 + 端点使者）
> **日期**：2026-04-02
