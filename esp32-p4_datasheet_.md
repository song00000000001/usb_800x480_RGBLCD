# ESP32-P4 系列芯片

# 技术规格书 预发布 v0.5

搭载 RISC-V 32 位双核高性能处理器与单核低功耗处理器的 MCU

强大的图像与语音处理能力

芯片封装内可叠封 16 MB 或 32 MB PSRAM

55 个 GPIO，丰富的外设

QFN104 (10×10 mm) 封装

包括：

ESP32-P4NRW16X 

ESP32-P4NRW32X 

# 产品概述

ESP32-P4 是一款高性能 MCU，支持超大片上内存，具有强大的图像和语音处理能力。该款 MCU 包含一个高性能 (HP) 系统和一个低功耗 (LP) 系统。HP 系统由 RISC-V 双核处理器驱动包含丰富的外设；LP 系统由 RISC-V 单核处理器驱动其外设针对低功耗应用进行了优化。

芯片的功能框图如下图所示。更多关于功耗的信息请参考章节 4.1.4.6 低功耗管理。

# ESP32-P4 — Espressif’s High Performance MCU

# HP Core System

RISC-V 32-bit Dual-core Microprocessor 400 MHz 

2-level Cache 

JTAG 

HPSPM L2MEM 

L2 ROM 

# LP Core System

RISC-V 32-bit Single-core Microprocessor 40 MHz 

LPSPM LPROM 

JTAG 

# Low Power System

Power Management U n it 

BAT Power Supply 

# H P Peri pherals

SPI 

I2C 

DIG ADC Controller 

ISP 

PPA 

# LP Peripherals

LP SPI 

LP I2C 

LP I2S 

LP Mai l box 

LP GPIO 

LP UART 

LP DIG ADC Controller 

eFuse Controller 

GP & WDT & LP Timers & Super WDT 

Temperature Sensor 

Touch Sensor 

# Security

SHA 

RSA DS 

ECC 

HMAC 

TEE 

TRNG 

DSA DS 

AES 

Digital Signature 

XTS AES 

PM P and PMA 

Secu re Boot 

H U K and Key Manager 

4096-bit OTP 

GPIO 

TWAI® 

Pulse Counter 

RMT 

PEG Codec 

MIPI CSI MIPI CSI 

GDMA 

LED PWM 

DW-GDMA 

SOC ETM 

Parallel IO ParallelIO ParallelIO

Camera 

MCPWM MCPWM 

OSE/SE 2.0 

LCD I LCDI 

te rface terface 

MIPI DSI MIPI DSI 

G P Timers 

System Timer SystemTimer 

WDT WDT 

Ethernet Ethernet 

Brownout Brownout 

Debug Probe Debug Probe 

Mod u les havi ng power i n specific power modes: 

 

# 产品特性

# CPU 和存储

用于 HP 系统的 RISC-V 32 位双核处理器，主频高达 400 MHz

用于 LP 系统的 RISC-V 32 位单核处理器，主频高达 40 MHz

CoreMark® 得分（双核）：

– 6.92 CoreMark/MHz 

128 KB HP ROM 

16 KB LP ROM 

• 768 KB HP L2MEM 

32 KB LP SRAM 

8 KB 暂存内存 (SPM)

• 多个高速外部存储器接口

两级高速缓存

# 系统 DMA

GDMA 控制器

• VDMA 控制器

• 2D-DMA 控制器

# 高级外设接口和传感器

55 个可编程 GPIO

– 5 个作为 strapping 管脚

图像处理子系统：

– JPEG 图像编解码器

– 图像信号处理器 (ISP)

– 像素处理加速器 (PPA)

– LCD 与 Camera 控制器

– H264 编码器

– MIPI 相机串行接口

– MIPI 显示串行接口

数字接口及外设：

– 5 个 UART

– LP UART 

– 4 个 SPI

– LP SPI 

– 2 个 I2C

– LP I2C 

– 模拟 I2C

– I3C 

– 3 个 I2S

– LP I2S 

– 脉冲计数器 (PCNT)

– USB 2.0 高速 OTG

– USB 2.0 全速 OTG

– USB 串口/JTAG 控制器

– 以太网介质访问控制器 (EMAC)

– 双线汽车接口 (TWAI)

– SD/MMC 主机控制器 (SDHOST)

– LED PWM 控制器 (LEDC)

– 2 个电机控制脉宽调制器 (MCPWM)

– 红外遥控 (RMT)

– 并行 IO 控制器 (PARLIO)

– 比特调节器

– 语音活动检测 (VAD)

模拟外设及传感器：

– 触摸传感器

– 温度传感器

– 2 个 ADC 控制器

– 模拟电压比较器

定时器：

– 2 个 52 位 HP 系统定时器

– 4 个 54 位 HP 通用定时器

– 2 个 32 位 HP 看门狗定时器 (MWDT)

– 32 位 LP 看门狗定时器 (RWDT)

– 模拟超级看门狗定时器 (SWD)

– 48 位 LP 通用定时器 (RTC Timer)

# 安全机制

• 安全启动

eFuse OTP 提供的一次性写入安全性

加密和安全组件：

– AES 加速器

– ECC 加速器

– HMAC 加速器

– RSA 加速器

– SHA 加速器

– RSA 数字签名外设 (RSA_DS)

– ECDSA 数字签名外设 (ECDSA_DS)

– 片外存储器加密与解密 (XTS_AES)

– 真随机数生成器 (TRNG)

• 密钥管理器

– 基于 SRAM PUF 的 HUK 生成

– 安全密钥管理

• 权限控制 (PMS)

# 应用

低功耗芯片 ESP32-P4 专为物联网 (IoT) 设备而设计，应用领域包括：

智能家居

工业自动化

医疗保健

消费电子产品

智慧农业

零售自助终端（POS、售货机）

服务机器人

多媒体播放器

摄像头视频流传输

高速 USB 主机与设备

智能语音交互终端

边缘视觉 AI 处理器

HMI 控制面板

# 目录

# 产品概述 2

产品特性 3

应用 5

# ESP32-P4 系列型号对比 11

1.1 命名规则 11

1.2 型号对比 11

1.3 芯片版本 11

# 2 管脚 12

2.1 管脚布局 12

2.2 管脚概述 13

2.3 IO 管脚 17

2.3.1 IO MUX 功能 17

2.3.2 LP IO MUX 功能 21

2.3.3 模拟功能 22

2.3.4 GPIO 和 LP GPIO 的限制 24

2.4 专用接口管脚 25

2.5 模拟管脚 27

2.6 电源 28

2.6.1 电源管脚 28

2.6.2 电源管理 28

2.6.3 芯片上电和复位 29

2.7 芯片与 flash 的管脚对应关系 31

# 3 启动配置项 32

3.1 芯片启动模式控制 33

3.2 VDDO_FLASH 电压控制 33

3.3 ROM 日志打印控制 34

3.4 JTAG 信号源控制 34

# 4 功能描述 36

4.1 系统 36

4.1.1 微处理器和主控 36

4.1.1.1 高性能处理器 36

4.1.1.2 RISC-V 追踪编码器 (TRACE) 36

4.1.1.3 处理器指令拓展 37

4.1.1.4 低功耗处理器 38

4.1.2 系统 DMA 38

4.1.2.1 通用 DMA 控制器 (GDMA-AHB, GDMA-AXI) 38

4.1.2.2 VDMA 控制器 (VDMA) 39

4.1.2.3 2D-DMA 控制器 (2D-DMA) 40

4.1.3 存储器组织结构 40

4.1.3.1 系统和存储器 41

4.1.3.2 eFuse 控制器 (eFuse) 42

4.1.3.3 Cache 43 

4.1.4 系统组件 43

4.1.4.1 GPIO 交换矩阵和 IO MUX 43

4.1.4.2 复位 44

4.1.4.3 时钟 45

4.1.4.4 中断矩阵 45

4.1.4.5 事件任务矩阵 45

4.1.4.6 低功耗管理 46

4.1.4.7 系统定时器 46

4.1.4.8 定时器组 (TIMG) 47

4.1.4.9 看门狗定时器 (WDT) 47

4.1.4.10 实时时钟定时器 48

4.1.4.11 权限控制 (PMS) 48

4.1.4.12 系统寄存器 48

4.1.4.13 辅助调试 49

4.1.4.14 LP 信箱控制器 49

4.1.4.15 欠压检测器 49

4.1.5 加密和安全组件 50

4.1.5.1 AES 加速器 (AES) 50

4.1.5.2 ECC 加速器 (ECC) 50

4.1.5.3 HMAC 加速器 (HMAC) 51

4.1.5.4 RSA 加速器 (RSA) 51

4.1.5.5 SHA 加速器 (SHA) 51

4.1.5.6 RSA 数字签名外设 (RSA_DS) 52

4.1.5.7 ECDSA 数字签名外设 (ECDSA_DS) 52

4.1.5.8 片外存储器加密与解密 (XTS_AES) 53

4.1.5.9 随机数发生器 (RNG) 53

4.1.5.10 密钥管理器 53

4.2 外设 55

4.2.1 图像处理 55

4.2.1.1 JPEG 图像编解码器 55

4.2.1.2 图像信号处理器 (ISP) 56

4.2.1.3 像素处理加速器 (PPA) 57

4.2.1.4 LCD 与 Camera 控制器 (LCD_CAM) 57

4.2.1.5 H264 编码器 58

4.2.1.6 MIPI 相机串行接口 59

4.2.1.7 MIPI 显示串行接口 59

4.2.2 通讯接口 59

4.2.2.1 UART 控制器 (UART) 60

4.2.2.2 SPI 控制器 (SPI) 60

4.2.2.3 I2C 控制器 (I2C) 63

4.2.2.4 模拟 I2C 控制器 63

4.2.2.5 I3C 控制器 63

4.2.2.6 I2S 控制器 (I2S) 64

4.2.2.7 LP I2S 控制器 65

4.2.2.8 脉冲计数控制器 (PCNT) 65

4.2.2.9 USB 2.0 高速 OTG 66

4.2.2.10 USB 2.0 全速 OTG 67

4.2.2.11 USB 串口/JTAG 控制器 (USB_SERIAL_JTAG) 68

4.2.2.12 以太网介质访问控制器 (EMAC) 69

4.2.2.13 双线汽车接口 (TWAI) 70

4.2.2.14 SD/MMC 主机控制器 (SDHOST) 71

4.2.2.15 LED PWM 控制器 (LEDC) 72

4.2.2.16 电机控制脉宽调制器 (MCPWM) 72

4.2.2.17 红外遥控 (RMT) 72

4.2.2.18 并行 IO 控制器 (PARLIO) 73

4.2.2.19 比特调节器 74

# 4.2.3 模拟信号处理 75

4.2.3.1 触摸传感器 75

4.2.3.2 温度传感器 (TSENS) 75

4.2.3.3 ADC 控制器 (ADC) 76

4.2.3.4 模拟电压比较器 76

4.2.3.5 语音活动检测 (VAD) 77

# 5 电气特性 78

5.1 绝对最大额定值 78

5.2 建议工作条件 78

5.3 VDDO_FLASH 输出特性 79

5.4 直流电气特性 (3.3 V, 25 °C) 79

5.5 ADC 特性 80

5.6 Active 模式与低功耗模式下的功耗 80

5.7 存储器规格 82

# 6 封装 84

# 相关文档和资源 85

# 附录 A – ESP32-P4 管脚总览 86

# 修订历史 89

# 表格

1-1 ESP32-P4 系列芯片对比 11

2-1 管脚概述 13

2-2 通过 IO MUX 连接的外设信号 17

2-3 IO MUX 管脚功能 18

2-4 通过 LP IO MUX 连接的 LP 外设信号 21

2-5 LP IO MUX 功能 21

2-6 连接模拟功能的模拟信号 22

2-7 模拟功能 22

2-8 专用外设信号 25

2-9 专用接口管脚 25

2-10 模拟管脚 27

2-11 电源管脚 28

2-12 电压稳压器 29

2-13 上电和复位时序参数说明 30

2-14 芯片与封装外 flash 的管脚对应关系 31

3-1 Strapping 管脚默认配置 32

3-2 Strapping 管脚的时序参数说明 32

3-3 系统启动模式控制 33

3-4 VDDO_FLASH 电压控制 34

3-5 UART0 ROM 日志打印控制 34

3-6 USB 串口/JTAG ROM 日志打印控制 34

3-7 JTAG 信号源控制 35

4-1 UART 和 LP UART 特性区分 60

5-1 绝对最大额定值 78

5-2 建议工作条件 78

5-3 VDDO_FLASH 内部和输出特性 79

5-4 直流电气特性 (3.3 V, 25 °C) 79

5-5 ADC 特性 80

5-6 ADC 校准结果 80

5-7 Active 模式下的功耗 80

5-8 低功耗模式下的功耗 82

5-9 Flash 规格 82

5-10 PSRAM 规格 83

# 插图

1-1 ESP32-P4 系列芯片命名规则 11

2-1 ESP32-P4 管脚布局（俯视图） 12

2-2 ESP32-P4 电源管理 29

2-3 上电和复位时序参数图 29

3-1 Strapping 管脚的时序参数图 33

4-1 地址映射结构 41

6-1 QFN104 (10×10 mm) 封装 84

# 1 ESP32-P4 系列型号对比

# 1.1 命名规则




# 1.2 型号对比


表 1-1. ESP32-P4 系列芯片对比


| 物料编号1 | 封装内 PSRAM | 环境温度2 (℃) | VDD_PSRAM_0/1 电压3 | 芯片版本 |
| --- | --- | --- | --- | --- |
| ESP32-P4NRW16X | 16 MB (OPI/HPI)4 | -40 ~ 85 | 1.8 V | v3.0/v3.1 |
| ESP32-P4NRW32X | 32 MB (OPI/HPI)4 | -40 ~ 85 | 1.8 V | v3.0/v3.1 |


1 更多关于芯片丝印和包装的信息，请参考章节 6 封装。



2 环境温度指乐鑫芯片外部的推荐环境温度。



3 更多关于 VDD_PSRAM_0/1 的信息，请参考章节 2.6 电源。



4 PSRAM 的 OPI 支持每个传输周期传输八位命令、地址和数据；HPI 支持每个传输周期传输八位命令和地址，以及十六位数据。更多关于 SPI 模式的信息，请参考章节 2.7 芯片与 flash 的管脚对应关系。


# 1.3 芯片版本

如表 1-1 型号对比 所示，ESP32-P4 有多个芯片版本投入市场，并使用相同的物料编号。

关于芯片版本的识别方式、支持特定芯片版本的 ESP-IDF 版本和每个芯片版本修复的错误，请参考《ESP32-P4 系列芯片勘误表》。

芯片版本 v3.x 较之前版本的主要变化，请参考《ESP32-P4 芯片版本 v3.x 使用指南》

# 2 管脚

# 2.1 管脚布局




# 2.2 管脚概述

ESP32-P4 芯片集成了多个需要与外界通讯的外设。由于芯片封装尺寸小、管脚数量有限，传送所有输入输出信号的唯一方法是管脚多路复用。管脚多路复用由软件可编程的寄存器控制（详见《ESP32-P4 技术参考手册》>章节 GPIO 交换矩阵和 IO MUX）。还有一些外设比较重要，ESP32-P4 芯片为其设置了专门用于连接这些外设的管脚，如 MIPI DSI 与 MIPI CSI 等。

总体而言，ESP32-P4 芯片的管脚可分为以下几类：

• IO 管脚，具有以下预设功能：

– 全部 IO 管脚预设了 IO MUX 功能 – 见表 2-3 IO MUX 功能

– 部分 IO 管脚预设了 LP IO MUX 功能 – 见表 2-5 LP IO MUX 功能

– 部分 IO 管脚预设了模拟功能 – 见表 2-7 模拟功能

预设功能即每个 IO 管脚直接连接至一组特定的片上组件信号。运行时，可通过映射寄存器配置连接管脚的组件信号。

• 专用接口管脚，只可用于特定外设，如 flash、MIPI DSI、MIPI CSI 等 – 见表 2-9 专用接口管脚

模拟管脚，专用于模拟功能 – 见表 2-10 模拟管脚

• 电源管脚，为芯片组件和非电源管脚供电 – 见表 2-11 电源管脚

表2-1管脚概述简要介绍了所有管脚。更多信息，详见下文相应章节，或参考附录A – ESP32-P4管脚总览。


表 2-1. 管脚概述


| 管脚序号 | 管脚名称 | 管脚类型 | 供电管脚2,3 | 管脚配置4 | 管脚功能1 |
| --- | --- | --- | --- | --- | --- |
| 复位时 | 复位后 | IO MUX | LP IO MUX | 模拟 |
| 1 | GPIO1 | IO | VDD_LP / VDD_BAT | - | - | IO MUX | LP IO MUX | 模拟 |
| 2 | GPIO2 | IO | VDD_LP / VDD_BAT | - | IE, WPU5 | IO MUX | LP IO MUX | 模拟 |
| 3 | GPIO3 | IO | VDD_LP / VDD_BAT | - | IE | IO MUX | LP IO MUX | 模拟 |
| 4 | GPIO4 | IO | VDD_LP | - | IE | IO MUX | LP IO MUX | 模拟 |
| 5 | GPIO5 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 6 | GPIO6 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 7 | GPIO7 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 8 | GPIO8 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 9 | VDD_LP | 电源 | - | - | - | - | - | - |
| 10 | GPIO9 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 11 | GPIO10 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 12 | GPIO11 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 13 | GPIO12 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 14 | GPIO13 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 15 | GPIO14 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 16 | GPIO15 | IO | VDD_LP | - | - | IO MUX | LP IO MUX | 模拟 |
| 17 | GPIO16 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 18 | GPIO17 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 19 | GPIO18 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 20 | GPIO19 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 21 | VDD_IO_0 | 电源 | - | - | - | - | - | - |

见下页


表 2-1 – 接上页


| 管脚序号 | 管脚名称 | 管脚类型 | 供电管脚2,3 | 管脚配置4 | 管脚功能1 |
| --- | --- | --- | --- | --- | --- |
| 复位时 | 复位后 | IO MUX | LP IO MUX | 模拟 |
| 22 | GPIO20 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 23 | GPIO21 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 24 | GPIO22 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 25 | GPIO23 | IO | VDD_IO_0 | - | - | IO MUX | - | 模拟 |
| 26 | VDD_HP_0 | 电源 | - | - | - | - | - | - |
| 27 | FLASH_CS | 专用 | VDD_FLASHIO | - | - | - | - | - |
| 28 | FLASH_Q | 专用 | VDD_FLASHIO | - | - | - | - | - |
| 29 | FLASH_WP | 专用 | VDD_FLASHIO | - | - | - | - | - |
| 30 | VDD_FLASHIO | 电源 | - | - | - | - | - | - |
| 31 | FLASH_HOLD | 专用 | VDD_FLASHIO | - | - | - | - | - |
| 32 | FLASH_CK | 专用 | VDD_FLASHIO | - | - | - | - | - |
| 33 | FLASH_D | 专用 | VDD_FLASHIO | - | - | - | - | - |
| 34 | DSI_REXT | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 35 | DSI_DATAP1 | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 36 | DSI_DATAN1 | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 37 | DSI_CLKN | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 38 | DSI_CLKP | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 39 | DSI_DATAPO | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 40 | DSI_DATANO | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 41 | VDD_MIPI_DPHY | 电源 | - | - | - | - | - | - |
| 42 | CSI_DATANO | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 43 | CSI_DATAPO | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 44 | CSI_CLKP | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 45 | CSI_CLKN | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 46 | CSI_DATAN1 | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 47 | CSI_DATAP1 | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 48 | CSI_REXT | 专用 | VDD_MIPI_DPHY | - | - | - | - | - |
| 49 | USB_DM | 专用 | VDD_USBPHY | - | - | - | - | - |
| 50 | USB_DP | 专用 | VDD_USBPHY | - | - | - | - | - |
| 51 | VDD_USBPHY | 电源 | - | - | - | - | - | - |
| 52 | GPIO24 | IO | VDD_IO_4 | - | - | IO MUX | - | 模拟 |
| 53 | GPIO25 | IO | VDD_IO_4 | - | USB_PU | IO MUX | - | 模拟 |
| 54 | VDD_HP_1 | 电源 | - | - | - | - | - | - |
| 55 | GPIO26 | IO | VDD_IO_4 | - | - | IO MUX | - | 模拟 |
| 56 | GPIO27 | IO | VDD_IO_4 | - | - | IO MUX | - | 模拟 |
| 57 | GPIO28 | IO | VDD_IO_4 | - | - | IO MUX | - | - |
| 58 | GPIO29 | IO | VDD_IO_4 | - | - | IO MUX | - | - |
| 59 | VDD_PSRAM_0 | 电源 | - | - | - | - | - | - |
| 60 | GPIO30 | IO | VDD_IO_4 | - | - | IO MUX | - | - |
| 61 | GPIO31 | IO | VDD_IO_4 | - | - | IO MUX | - | - |
| 62 | VDD_IO_4 | 电源 | - | - | - | - | - | - |
| 63 | GPIO32 | IO | VDD_IO_4 | IE | - | IO MUX | - | - |
| 64 | GPIO33 | IO | VDD_IO_4 | IE | - | IO MUX | - | - |
| 65 | GPIO34 | IO | VDD_IO_4 | IE | - | IO MUX | - | - |
| 66 | GPIO35 | IO | VDD_IO_4 | IE, WPU | - | IO MUX | - | - |


见下页



表 2-1 – 接上页


| 管脚序号 | 管脚名称 | 管脚类型 | 供电管脚2,3 | 管脚配置4 | 管脚功能1 |
| --- | --- | --- | --- | --- | --- |
| 复位时 | 复位后 | IO MUX | LP IO MUX | 模拟 |
| 67 | VDD_MSBRAM_1 | 电源 | - | - | - | - | - | - |
| 68 | GPIO36 | IO | VDD_IO_4 | IE | - | IO MUX | - | - |
| 69 | GPIO37 | IO | VDD_IO_4 | IE | - | IO MUX | - | - |
| 70 | GPIO38 | IO | VDD_IO_4 | IE | - | IO MUX | - | - |
| 71 | VDDO_FLASH | 电源 | - | - | - | - | - | - |
| 72 | VDDO_MSBRAM | 电源 | - | - | - | - | - | - |
| 73 | VDDO_3 | 电源 | - | - | - | - | - | - |
| 74 | VDDO_4 | 电源 | - | - | - | - | - | - |
| 75 | VDD_LDO | 电源 | - | - | - | - | - | - |
| 76 | VDD_HP_2 | 电源 | - | - | - | - | - | - |
| 77 | VDD_DCDCC | 电源 | - | - | - | - | - | - |
| 78 | FB_DCDC | 模拟 | - | - | - | - | - | - |
| 79 | EN_DCDC | 模拟 | - | - | - | - | - | - |
| 80 | GPIO39 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 81 | GPIO40 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 82 | GPIO41 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 83 | GPIO42 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 84 | GPIO43 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 85 | VDD_IO_5 | 电源 | - | - | - | - | - | - |
| 86 | GPIO44 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 87 | GPIO45 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 88 | GPIO46 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 89 | GPIO47 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 90 | GPIO48 | IO | VDD_IO_5 | - | - | IO MUX | - | - |
| 91 | VDD_HP_3 | 电源 | - | - | - | - | - | - |
| 92 | GPIO49 | IO | VDD_IO_6 | - | - | IO MUX | - | 模拟 |
| 93 | GPIO50 | IO | VDD_IO_6 | - | - | IO MUX | - | 模拟 |
| 94 | GPIO51 | IO | VDD_IO_6 | - | - | IO MUX | - | 模拟 |
| 95 | GPIO52 | IO | VDD_IO_6 | - | - | IO MUX | - | 模拟 |
| 96 | VDD_IO_6 | 电源 | - | - | - | - | - | - |
| 97 | GPIO53 | IO | VDD_IO_6 | - | - | IO MUX | - | 模拟 |
| 98 | GPIO54 | IO | VDD_IO_6 | - | - | IO MUX | - | 模拟 |
| 99 | XTAL_N | 模拟 | - | - | - | - | - | - |
| 100 | XTAL_P | 模拟 | - | - | - | - | - | - |
| 101 | VDD_ANA | 电源 | - | - | - | - | - | - |
| 102 | VDD_BAT | 电源 | - | - | - | - | - | - |
| 103 | CHIPPU | 模拟 | - | - | - | - | - | - |
| 104 | GPIO0 | IO | VDD_LP / VDD_BAT | - | - | IO MUX | LP IO MUX | 模拟 |
| 105 | GND | 电源 | - | - | - | - | - | - |


1. 加粗功能为默认启动模式下管脚的默认功能，详见章节 3.1 芯片启动模式控制。



2. 供电管脚一栏，由 VDD_LP / VDD_BAT 供电的管脚：



供电管脚（VDD_LP 或 VDD_BAT）可通过寄存器配置。


3. GPIO24 与 GPIO25 的默认驱动电流为 40 mA。除 GPIO24 与 GPIO25 外，其他管脚的默认驱动电流为 20 mA。

4. 管脚配置一栏为复位时和复位后预设配置缩写：

IE – 输入使能

WPU – 内部弱上拉电阻使能

USB_PU – USB 上拉电阻使能

– USB 管脚（GPIO24/26 和 GPIO25/27）默认开启 USB 功能，此时管脚是否上拉由 USB 上拉决定。USB 上拉由 USB_SERIAL_JTAG_DP/DM_PULLUP 控制，USB 上拉电阻的具体阻值可通过 USB_SERIAL_JTAG_PULLUP_VALUE 位控制。

– USB 管脚关闭 USB 功能时，用作普通 GPIO，默认禁用管脚内部弱上/下拉电阻，可通过 IO_MUX_GPIOx_FUN_WPU/WPD配置。

# 5. EFUSE_DIS_PAD_JTAG 的值为

• 0（初始默认值），管脚复位后输入使能，上拉电阻使能 ( |E = 1|, WPU = ↑ )

• 1 管脚复位后输入关闭，高阻 (|E = 0⟩)

# 2.3 IO 管脚

# 2.3.1 IO MUX 功能

IO MUX 能让一个输入/输出管脚连接多个输入/输出信号。ESP32-P4 的每个 IO 管脚可在表 2-3 IO MUX 功能 列出的四个信号（IO MUX 功能，即 F0~F3）中选择，连接任意一个。

四个信号中：

部分源自 GPIO 交换矩阵（GPIO0、GPIO1等）。GPIO 交换矩阵包含内部信号传输线路，用于映射信号，能令管脚连接几乎任一外设信号。这种映射虽然灵活，但可能影响传输信号的速度，造成延迟。

部分直接源自特定外设（U0TXD、MTCK 等），包括 UART0、JTAG、SPI2 等 - 详见表 2-2 IO MUX 功能。


表 2-2. 通过 IO MUX 连接的外设信号


| 管脚功能 | 信号 | 描述 |
| --- | --- | --- |
| MTCK | 测试时钟 (Test clock) |  |
| MTDO | 测试数据输出 (Test data out) | 用于调试功能的 JTAG 接口 |
| MTDI | 测试数据输入 (Test data in) |  |
| MTMS | 测试模式选择 (Test mode select) |  |
| SPI2_HOLDPAD | 暂停 (Hold) |  |
| SPI2_CSPAD | 片选 (Chip select) | 3.3 V SPI2 接口,既可以配置成主机模式,又可以配置成从机模式。支持单线,二线,四线或八线通信模式(八线通信模式仅在主机模式下有效)。 |
| SPI2_DPAD | 数据输入 (Data in) |  |
| SPI2_CKPAD | 时钟 (Clock) |  |
| SPI2_QPAD | 数据输出 (Data out) |  |
| SPI2_WPPAD | 写保护 (Write protect) |  |
| SPI2_IO...PAD | 数据 (Data) | 八线 SPI 模式下 SPI2 接口的高 4 位数据线接口及DQS 接口 |
| SPI2_DQSPAD | 数据选通/数据掩码 (Data strobe/data mask) |  |
| UARTO_TXDPAD | 发送数据 (Transmit data) | UARTO 接口 |
| UARTO_RXDPAD | 接收数据 (Receive data) |  |
| REF_50M_CLKPAD | 50 MHz 参考时钟输出 | 用于给芯片外部或内部模块提供 50 MHz 时钟 |
| GMAC_PHY_RXDV PAD1 | 接收数据有效 (Receive data valid) |  |
| GMAC_PHY_RXD...PAD | 接收数据线 0/1 |  |
| GMAC_PHY_RXERPAD | 接收错误 (Receive error) |  |
| GMAC_PHY_TXDV PAD | 发送数据有效 (Transmit data valid) |  |
| GMAC_PHY_TXD...PAD | 发送数据线 0/1 | RMII Ethernet PHY 接口 |
| GMAC_PHY_TXERPAD | 发送错误 (Transmit error) |  |
| GMAC_PHY_TXENPAD | 发送使能 (Transmit enable) |  |
| GMAC_RMII_CLKPAD | RMII 接口时钟 (Clock) |  |
| SD1_CDATA...PAD | SD1 卡数据线 0~7 |  |
| SD1_CCLKPAD | SD1 卡时钟 (Card clock) | SDIO3.0 接口 |
| SD1_CCMDPAD | SD1 卡命令 (Card command) |  |


1 PAD 层不区分 MII 或 RMII 接口。该信号在 MII 模式下用作 RX_DV，在 RMII 模式下用作 CRS_DV。


表 2-3 IO MUX 功能 列出了管脚的 IO MUX 功能。


表 2-3. IO M UX 管脚功能


| 管脚序号 | IO MUX / GPIO名称2 | IO MUX 功能1,2,3 |
| --- | --- | --- |
| FO | 类型3 | F1 | 类型 | F2 | 类型 | F3 | 类型 |
| 1 | GPIO1 | GPIO1 | I/O/T | GPIO1 | I/O/T | - | - | - | - |
| 2 | GPIO2 | MTCK | I1 | GPIO2 | I/O/T | - | - | - | - |
| 3 | GPIO3 | MTDI | I1 | GPIO3 | I/O/T | - | - | - | - |
| 4 | GPIO4 | MTMS | I0 | GPIO4 | I/O/T | - | - | - | - |
| 5 | GPIO5 | MTDO | O/T | GPIO5 | I/O/T | - | - | - | - |
| 6 | GPIO6 | GPIO6 | I/O/T | GPIO6 | I/O/T | - | - | SPI2_HOLDPAD | I1/O/T |
| 7 | GPIO7 | GPIO7 | I/O/T | GPIO7 | I/O/T | - | - | SPI2_CSPAD | I1/O/T |
| 8 | GPIO8 | GPIO8 | I/O/T | GPIO8 | I/O/T | - | - | SPI2_DPAD | I1/O/T |
| 10 | GPIO9 | GPIO9 | I/O/T | GPIO9 | I/O/T | - | - | SPI2_CKPAD | I1/O/T |
| 11 | GPIO10 | GPIO10 | I/O/T | GPIO10 | I/O/T | - | - | SPI2_QPAD | I1/O/T |
| 12 | GPIO11 | GPIO11 | I/O/T | GPIO11 | I/O/T | - | - | SPI2_WPPAD | I1/O/T |
| 13 | GPIO12 | GPIO12 | I/O/T | GPIO12 | I/O/T | - | - | - | - |
| 14 | GPIO13 | GPIO13 | I/O/T | GPIO13 | I/O/T | - | - | - | - |
| 15 | GPIO14 | GPIO14 | I/O/T | GPIO14 | I/O/T | - | - | - | - |
| 16 | GPIO15 | GPIO15 | I/O/T | GPIO15 | I/O/T | - | - | - | - |
| 17 | GPIO16 | GPIO16 | I/O/T | GPIO16 | I/O/T | - | - | - | - |
| 18 | GPIO17 | GPIO17 | I/O/T | GPIO17 | I/O/T | - | - | - | - |
| 19 | GPIO18 | GPIO18 | I/O/T | GPIO18 | I/O/T | - | - | - | - |
| 20 | GPIO19 | GPIO19 | I/O/T | GPIO19 | I/O/T | - | - | - | - |
| 22 | GPIO20 | GPIO20 | I/O/T | GPIO20 | I/O/T | - | - | - | - |
| 23 | GPIO21 | GPIO21 | I/O/T | GPIO21 | I/O/T | - | - | - | - |
| 24 | GPIO22 | GPIO22 | I/O/T | GPIO22 | I/O/T | - | - | - | - |
| 25 | GPIO23 | GPIO23 | I/O/T | GPIO23 | I/O/T | - | - | REF_50M_CLKPAD | O |
| 52 | GPIO24 | GPIO24 | I/O/T | GPIO24 | I/O/T | - | - | - | - |
| 53 | GPIO25 | GPIO25 | I/O/T | GPIO25 | I/O/T | - | - | - | - |
| 55 | GPIO26 | GPIO26 | I/O/T | GPIO26 | I/O/T | - | - | - | - |

见下页


表 2-3 – 接上页


| 管脚序号 | IO MUX / GPIO名称2 | IO MUX 功能1,2,3 |
| --- | --- | --- |
| F0 | 类型3 | F1 | 类型 | F2 | 类型 | F3 | 类型 |
| 56 | GPIO27 | GPIO27 | I/O/T | GPIO27 | I/O/T | - | - | - | - |
| 57 | GPIO28 | GPIO28 | I/O/T | GPIO28 | I/O/T | SPI2_CS_pad | I1/O/T | GMAC_PHY_RXDV_pad | IO |
| 58 | GPIO29 | GPIO29 | I/O/T | GPIO29 | I/O/T | SPI2_D_pad | I1/O/T | GMAC_PHY_RXDO_pad | IO |
| 60 | GPIO30 | GPIO30 | I/O/T | GPIO30 | I/O/T | SPI2_CK_pad | I1/O/T | GMAC_PHY_RXD1_pad | IO |
| 61 | GPIO31 | GPIO31 | I/O/T | GPIO31 | I/O/T | SPI2_Q_pad | I1/O/T | GMAC_PHY_RXER_pad | IO |
| 63 | GPIO32 | GPIO32 | I/O/T | GPIO32 | I/O/T | SPI2_HOLD_pad | I1/O/T | GMAC_RMII_CLK_pad | IO |
| 64 | GPIO33 | GPIO33 | I/O/T | GPIO33 | I/O/T | SPI2_WP_pad | I1/O/T | GMAC_PHY_TXEN_pad | O |
| 65 | GPIO34 | GPIO34 | I/O/T | GPIO34 | I/O/T | SPI2_IO4_pad | I1/O/T | GMAC_PHY_TXDO_pad | O |
| 66 | GPIO35 | GPIO35 | I/O/T | GPIO35 | I/O/T | SPI2_IO5_pad | I1/O/T | GMAC_PHY_TXD1_pad | O |
| 68 | GPIO36 | GPIO36 | I/O/T | GPIO36 | I/O/T | SPI2_IO6_pad | I1/O/T | GMAC_PHY_TXER_pad | O |
| 69 | GPIO37 | UARTO_TXD_pad | O | GPIO37 | I/O/T | SPI2_IO7_pad | I1/O/T | - | - |
| 70 | GPIO38 | UARTO_RXD_pad | I1 | GPIO38 | I/O/T | SPI2_DQS_pad | O/T | - | - |
| 80 | GPIO39 | SD1_CDATAO_pad | I1/O/T | GPIO39 | I/O/T | - | - | REF_50M_CLK_pad | O |
| 81 | GPIO40 | SD1_CDATA1_pad | I1/O/T | GPIO40 | I/O/T | - | - | GMAC_PHY_TXEN_pad | O |
| 82 | GPIO41 | SD1_CDATA2_pad | I1/O/T | GPIO41 | I/O/T | - | - | GMAC_PHY_TXDO_pad | O |
| 83 | GPIO42 | SD1_CDATA3_pad | I1/O/T | GPIO42 | I/O/T | - | - | GMAC_PHY_TXD1_pad | O |
| 84 | GPIO43 | SD1_CCLK_pad | O | GPIO43 | I/O/T | - | - | GMAC_PHY_TXER_pad | O |
| 86 | GPIO44 | SD1_CCMD_pad | I1/O/T | GPIO44 | I/O/T | - | - | GMAC_RMII_CLK_pad | IO |
| 87 | GPIO45 | SD1_CDATA4_pad | I1/O/T | GPIO45 | I/O/T | - | - | GMAC_PHY_RXDV_pad | IO |
| 88 | GPIO46 | SD1_CDATA5_pad | I1/O/T | GPIO46 | I/O/T | - | - | GMAC_PHY_RXDO_pad | IO |
| 89 | GPIO47 | SD1_CDATA6_pad | I1/O/T | GPIO47 | I/O/T | - | - | GMAC_PHY_RXD1_pad | IO |
| 90 | GPIO48 | SD1_CDATA7_pad | I1/O/T | GPIO48 | I/O/T | - | - | GMAC_PHY_RXER_pad | IO |
| 92 | GPIO49 | GPIO49 | I/O/T | GPIO49 | I/O/T | - | - | GMAC_PHY_TXEN_pad | O |
| 93 | GPIO50 | GPIO50 | I/O/T | GPIO50 | I/O/T | - | - | GMAC_RMII_CLK_pad | IO |
| 94 | GPIO51 | GPIO51 | I/O/T | GPIO51 | I/O/T | - | - | GMAC_PHY_RXDV_pad | IO |
| 95 | GPIO52 | GPIO52 | I/O/T | GPIO52 | I/O/T | - | - | GMAC_PHY_RXDO_pad | IO |
| 97 | GPIO53 | GPIO53 | I/O/T | GPIO53 | I/O/T | - | - | GMAC_PHY_RXD1_pad | IO |

见下页


表 2-3 – 接上页


| 管脚序号 | IO MUX / GPIO名称2 | IO MUX功能1,2,3 |
| --- | --- | --- |
| F0 | 类型3 | F1 | 类型 | F2 | 类型 | F3 | 类型 |
| 98 | GPIO54 | GPIO54 | I/O/T | GPIO54 | I/O/T | - | - | GMAC_PHY_RXERPAD | IO |
| 104 | GPIO0 | GPIO0 | I/O/T | GPIO0 | I/O/T | - | - | - | - |

1 加粗表示默认启动模式下的默认管脚功能，详见章节 3.1 芯片启动模式控制。

2 高亮的单元格，详见章节 2.3.4 GPIO 和 LP GPIO 的限制。

3 每个 IO MUX 功能 (Fn，= {O} ~ 3) 均对应一个 “类型”。 以下是各个 “类型” 的含义：

• I – 输入。 O – 输出。 T – 高阻。

• I1 – 输入；如果该管脚分配了 Fn 以外的功能，则 Fn 的输入信号恒为 1。

• I0 – 输入；如果该管脚分配了 Fn 以外的功能，则 Fn 的输入信号恒为 0。

# 2.3.2 LP IO MUX 功能

芯片处于 Deep-sleep 模式时，章节 2.3.1 IO MUX 功能 介绍的 IO 管脚功能无法使用。这正是引入 LP IO MUX 的原因。LP IO 管脚连接 LP 系统，由 VDD_LP 或 VDD_BAT 供电，使用 LP IO MUX 能在 Deep-sleep 模式下让一个 LP 输入/输出管脚连接多个输入/输出信号。

LP IO 管脚具有 LP IO MUX 功能，可以

• 用作 LP GPIO（LP_GPIO0、LP_GPIO1 等），连接 LP 处理器

• 或者连接 LP 外设信号（LP_UART_TXD_PAD、LP_UART_RXD_PAD）- 见表 2-4 LP IO MUX 功能


表 2-4. 通过 LP IO MUX 连接的 LP 外设信号


| 管脚功能 | 信号 | 描述 |
| --- | --- | --- |
| LP_UART_TXD_PAD | 发送数据(Transmit data) | LP_UART 接口 |
| LP_UART_RXD_PAD | 接收数据(Receive data) |

表 2-5 LP IO MUX 功能 列出了 LP IO 管脚的 LP 功能。


表 2-5. LP IO MUX 功能


| 管脚序号 | LP IO名称1 | LP IO MUX 功能 |
| --- | --- | --- |
| F0 | 类型 | F1 | 类型 |
| 1 | LP_GPIO1 | LP_G PIO1 | I/O/T | LP_G PIO1 | I/O/T |
| 2 | LP_G PIO2 | LP_G PIO2 | I/O/T | LP_G PIO2 | I/O/T |
| 3 | LP_G PIO3 | LP_G PIO3 | I/O/T | LP_G PIO3 | I/O/T |
| 4 | LP_G PIO4 | LP_G PIO4 | I/O/T | LP_G PIO4 | I/O/T |
| 5 | LP_G PIO5 | LP_G PIO5 | I/O/T | LP_G PIO5 | I/O/T |
| 6 | LP_G PIO6 | LP_G PIO6 | I/O/T | LP_G PIO6 | I/O/T |
| 7 | LP_G PIO7 | LP_G PIO7 | I/O/T | LP_G PIO7 | I/O/T |
| 8 | LP_G PIO8 | LP_G PIO8 | I/O/T | LP_G PIO8 | I/O/T |
| 10 | LP_G PIO9 | LP_G PIO9 | I/O/T | LP_G PIO9 | I/O/T |
| 11 | LP_G PIO10 | LP_G PIO10 | I/O/T | LP_G PIO10 | I/O/T |
| 12 | LP_G PIO11 | LP_G PIO11 | I/O/T | LP_G PIO11 | I/O/T |
| 13 | LP_G PIO12 | LP_G PIO12 | I/O/T | LP_G PIO12 | I/O/T |
| 14 | LP_G PIO13 | LP_G PIO13 | I/O/T | LP_G PIO13 | I/O/T |
| 15 | LP_UART_TXD_pad | LP_UART_TXD_pad | O | LP_G PIO14 | I/O/T |
| 16 | LP_UART_RXD_pad | LP_UART_RXD_pad | I1 | LP_G PIO15 | I/O/T |
| 104 | LP_G PIO0 | LP_G PIO0 | I/O/T | LP_G PIO0 | I/O/T |


1 由于 LP 功能通过使用 LP GPIO 编号的 LP GPIO 寄存器配置，此列列出的是 LP GPIO的名称。


# 2.3.3 模拟功能

部分 IO 管脚具有模拟功能，可用于任意功耗模式下的模拟外设（如触摸传感器、ADC）。模拟功能连接内部模拟信号，详见表 2-6 模拟功能。


表 2-6. 连接模拟功能的模拟信号


| 管脚功能 | 信号 | 描述 |
| --- | --- | --- |
| XTAL_32K_N | 负极性时钟信号(Negative clock signal) | 连接有源晶振的外部32kHz时钟输入/输出 |
| XTAL_32K_P | 正极性时钟信号(Positive clock signal) |
| TOUCH_CHANNEL... | 触摸传感器通道信号 | 触摸传感器接口 |
| ADC...CHANNEL... | ADC1/2通道信号 | ADC1/2接口 |
| USB1P1_N... | USB D- | USB 2.0全速OTG接口和USB串口/JTAG功能 |
| USB1P1_P... | USB D+ |
| ANA_COMP... | P0/P1电压 | 模拟电压比较器0/1接口 |


表 2-7 模拟功能 列出了 IO 管脚的模拟功能。



表 2-7. 模拟功能


| 管脚序号 | 模拟IO名称 | 模拟功能1 |
| --- | --- | --- |
| FO | F1 |
| 1 | GPIO1 | XTAL_32K_P | - |
| 2 | GPIO2 | TOUCH_CHANNEL1 | - |
| 3 | GPIO3 | TOUCH_CHANNEL2 | - |
| 4 | GPIO4 | TOUCH_CHANNEL3 | - |
| 5 | GPIO5 | TOUCH_CHANNEL4 | - |
| 6 | GPIO6 | TOUCH_CHANNEL5 | - |
| 7 | GPIO7 | TOUCH_CHANNEL6 | - |
| 8 | GPIO8 | TOUCH_CHANNEL7 | - |
| 10 | GPIO9 | TOUCH_CHANNEL8 | - |
| 11 | GPIO10 | TOUCH_CHANNEL9 | - |
| 12 | GPIO11 | TOUCH_CHANNEL10 | - |
| 13 | GPIO12 | TOUCH_CHANNEL11 | - |
| 14 | GPIO13 | TOUCH_CHANNEL12 | - |
| 15 | GPIO14 | TOUCH_CHANNEL13 | - |
| 16 | GPIO15 | TOUCH_CHANNEL14 | - |
| 17 | GPIO16 | ADC1_CHANNELLO | - |
| 18 | GPIO17 | ADC1_CHANNEL1 | - |
| 19 | GPIO18 | ADC1_CHANNEL2 | - |
| 20 | GPIO19 | ADC1_CHANNEL3 | - |
| 22 | GPIO20 | ADC1_CHANNEL4 | - |
| 23 | GPIO21 | ADC1_CHANNEL5 | - |
| 24 | GPIO22 | ADC1_CHANNEL6 | - |
| 25 | GPIO23 | ADC1_CHANNEL7 | - |

见下页


表 2-7 – 接上页


| 管脚 序号 | 模拟 IO名称 | 模拟功能1 |
| --- | --- | --- |
| F0 | F1 |
| 52 | GPIO24 | USB1P1_NO | - |
| 53 | GPIO25 | USB1P1_P0 | - |
| 55 | GPIO26 | USB1P1_N1 | - |
| 56 | GPIO27 | USB1P1_P1 | - |
| 92 | GPIO49 | ADC2_CHANNEL0 | - |
| 93 | GPIO50 | ADC2_CHANNEL1 | - |
| 94 | GPIO51 | ADC2_CHANNEL2 | ANA_COMPO |
| 95 | GPIO52 | ADC2_CHANNEL3 | ANA_COMPO |
| 97 | GPIO53 | ADC2_CHANNEL4 | ANA_COMP1 |
| 98 | GPIO54 | ADC2_CHANNEL5 | ANA_COMP1 |
| 104 | GPIO0 | XTAL_32K_N | - |

1 加粗表示默认启动模式下的默认管脚功能，详见章节3.1芯片启动模式控制。

2 高亮 的单元格，详见章节 2.3.4 GPIO 和 LP GPIO 的限制。

# 2.3.4 GPIO 和 LP GPIO 的限制

ESP32-P4 的所有 IO 管脚都有 GPIO 功能，部分还具有 LP GPIO 功能。不过，这些 IO 管脚是多功能管脚，可以根据需求配置不同的功能，也有一些使用限制，需要特别注意。

本章节的表格中，部分管脚功能有 高亮 标记。推荐优先使用没有高亮的 GPIO 或 LP GPIO 管脚。如需更多管脚，请谨慎选择高亮的 GPIO 或 LP GPIO 管脚，避免与重要功能冲突。

高亮的 IO 管脚具有以下重要功能之一：

• Strapping 管脚 – 启动时逻辑电平需为特定值。详见章节 3 启动配置项。

USB1P1_N0/P0 – 默认情况下连接 USB 串口/JTAG 控制器。此类管脚需重新配置，方可用作 GPIO。

JTAG 接口 – 通常用于调试功能。详见表 2-2 IO MUX 功能。要释放这类管脚，可用 USB 串口/JTAG 控制器的 USB1P1_N/P 功能代替。详见章节 3.4 JTAG 信号源控制。

UART 接口 – 通常用于调试功能。详见表 2-2 IO MUX 功能。

也可参考 附录 A – ESP32-P4 管脚总览。

# 2.4 专用接口管脚

由于一些外设功能比较重要，因此将一些管脚专用于连接这些外设，如 MIPI DSI，MIPI CSI 等。


表 2-8. 专用外设信号


| 管脚功能 | 信号 | 描述 |
| --- | --- | --- |
| FLASH_CS | 片选 (Chip select) |  |
| FLASH_Q | 数据输出 (Data output) |  |
| FLASH_WP | 写保护 (Write protect) | 用于连接 flash |
| FLASH_HOLD | 暂停 (Hold) |  |
| FLASH_CK | 时钟 (Clock) |  |
| FLASH_D | 数据输入 (Data in) |  |
| MIPI DSI PHY 4.02 kΩ EXTERNAL RESISTOR | 4.02 kΩ 外部电阻 |  |
| MIPI DSI PHY DATAP... | 数据正向通道 0/1 (Data positive channel 0/1) | MIPI DSI 接口 |
| MIPI DSI PHY DATAN... | 数据负向通道 0/1 (Data negative channel 0/1) |  |
| MIPI DSI PHY CLKN | 时钟负向通道 (Clock negative channel) |  |
| MIPI DSI PHY CLKP | 时钟正向通道 (Clock positive channel) |  |
| MIPI CSI PHY 4.02 kΩ EXTERNAL RESISTOR | 4.02 kΩ 外部电阻 |  |
| MIPI CSI PHY DATAP... | 数据正向通道 0/1 (Data positive channel 0/1) | MIPI CSI 接口 |
| MIPI CSI PHY DATAN... | 数据负向通道 0/1 (Data negative channel 0/1) |  |
| MIPI CSI PHY CLKN | 时钟负向通道 (Clock negative channel) |  |
| MIPI CSI PHY CLKP | 时钟正向通道 (Clock positive channel) |  |
| USB2 OTG PHY DM | USB D- | USB 2.0 高速 OTG 接口 |
| USB2 OTG PHY DP | USB D+ |


表 2-9 专用接口管脚 列出了专用接口管脚。



表 2-9. 专用接口管脚


| 管脚 序号 | 专用 接口管脚 | 功能1 |
| --- | --- | --- |
| FO | 类型 |
| 27 | FLASH_CS | FLASH_CS | O |
| 28 | FLASH_Q | FLASH_Q | I/O/T |
| 29 | FLASH_WP | FLASH_WP | I/O/T |
| 31 | FLASH_HOLD | FLASH_HOLD | I/O/T |
| 32 | FLASH_CK | FLASH_CK | O |
| 33 | FLASH_D | FLASH_D | I/O/T |
| 34 | DSI_REXT | MIPI DSI PHY 4.02 kΩ EXTERNAL RESISTOR | I/O/T |
| 35 | DSI_DATAP1 | MIPI DSI PHY DATAP1 | I/O/T |
| 36 | DSI_DATAN1 | MIPI DSI PHY DATAN1 | I/O/T |
| 37 | DSI_CLKN | MIPI DSI PHY CLKN | I/O/T |
| 38 | DSI_CLKP | MIPI DSI PHY CLKP | I/O/T |
| 39 | DSI_DATAPO | MIPI DSI PHY DATAPO | I/O/T |


见下页



表 2-9 – 接上页


| 管脚 序号 | 专用 接口管脚 | 功能1 |
| --- | --- | --- |
| F0 | 类型 |
| 40 | DSI_DATANO | MIPI DSI PHY DATANO | I/O/T |
| 42 | CSI_DATANO | MIPI CSI PHY DATANO | I/O/T |
| 43 | CSI_DATAPO | MIPI CSI PHY DATAPO | I/O/T |
| 44 | CSI_CLKP | MIPI CSI PHY CLKP | I/O/T |
| 45 | CSI_CLKN | MIPI CSI PHY CLKN | I/O/T |
| 46 | CSI_DATAN1 | MIPI CSI PHY DATAN1 | I/O/T |
| 47 | CSI_DATAP1 | MIPI CSI PHY DATAP1 | I/O/T |
| 48 | CSI_REXT | MIPI CSI PHY 4.02 kΩ EXTERNAL RESISTOR | I/O/T |
| 49 | USB_DM | USB2 OTG PHY DM | I/O/T |
| 50 | USB_DP | USB2 OTG PHY DP | I/O/T |

# 2.5 模拟管脚


表 2-10. 模拟管脚


| 管脚序号 | 管脚名称 | 管脚类型 | 管脚功能 |
| --- | --- | --- | --- |
| 78 | FB_DCDC | - | 外部DC/DC的反馈电源管脚，与外部DC/DC的反馈电阻一起调节VDD_HP_0/1/2/3的电压 |
| 79 | EN_DCDC | O | 外部DC/DC的使能管脚 |
| 99 | XTAL_N | - | 连接ESP32-P4有源晶振或无源晶振的外部时钟输入/输出。 |
| 100 | XTAL_P | - | P/N指差分时钟正极/负极端。 |
| 103 | CHIP_PU | I | 高电平:芯片使能(上电);低电平:芯片关闭(掉电);注意不能让CHIP_PU管脚浮空 |

# 2.6 电源

# 2.6.1 电源管脚

表 2-11 电源管脚 列举了为芯片供电的电源管脚。


表 2-11. 电源管脚


| 管脚序号 | 管脚名称 | 方向 | 电源1 |
| --- | --- | --- | --- |
| 电源域/其他3 | IO管脚 |
| 9 | VDD_LP | 输入 | LP电源域 | LP IO4 |
| 21 | VDD_IO_0 | 输入 | 数字电源域 | HP IO |
| 26 | VDD_HP_0 | 输入 | 数字电源域 |  |
| 30 | VDD_FLASHIO2 | 输入 | flash IO电源域 | flash IO |
| 41 | VDD_MIPI_DPHY | 输入 | MIPI PHY | MIPI IO |
| 51 | VDD_USBPHY | 输入 | USB PHY | 高速 USB IO |
| 54 | VDD_HP_1 | 输入 | 数字电源域 |  |
| 59 | VDD_PSRAM_0 | 输入 | PSRAM | PSRAM IO |
| 62 | VDD_IO_4 | 输入 | 数字电源域 | HP IO |
| 67 | VDD_PSRAM_1 | 输入 | PSRAM | PSRAM IO |
| 71 | VDDO_FLASH | 输出 | 封装外 flash,最大输出 50 mA 电流 |  |
| 72 | VDDO_PSRAM | 输出 | 封装内或封装外 PSRAM,最大输出 50 mA 电流 |  |
| 73 | VDDO_3 | 输出 | 最大输出 50 mA 电流 |  |
| 74 | VDDO_4 | 输出 | 最大输出 50 mA 电流 |  |
| 75 | VDD_LDO | 输入 | 模拟电源域,为电压稳压器提供电源 |  |
| 76 | VDD_HP_2 | 输入 | 数字电源域 |  |
| 77 | VDD_DCDCC | 输入 | 模拟电源域,为 DC/DC 控制部分提供电源 |  |
| 85 | VDD_IO_5 | 输入 | 数字电源域 | HP IO |
| 91 | VDD_HP_3 | 输入 | 数字电源域 |  |
| 96 | VDD_IO_6 | 输入 | 数字电源域 | HP IO |
| 101 | VDD_ANA | 输入 | 模拟电源域 |  |
| 102 | VDD_BAT | 输入 | 模拟电源域,可外接电池 |  |
| 105 | GND | - | 外部接地 |  |


1 请结合章节 2.6.2 电源管理 阅读。



2 VDD_FLASHIO 为 flash IO 供电，电压需根据具体 flash 型号调节，本文中所有相关的描述均以 3.3V 的 flash 为例。



3 电压、电流的推荐值和最大值，详见章节 5.1 绝对最大额定值 和章节 5.2 建议工作条件。



4 LP IO 管脚即由 VDD_LP 或 VDD_BAT 供电的管脚，如图 2-2 ESP32-P4 电源管理 所示，也可参考表 2-1 管脚概述 > 供电管脚一栏。


# 2.6.2 电源管理

电源管理如图 2-2 ESP32-P4 电源管理 所示。

芯片上的元器件通过电压稳压器供电。


表 2-12. 电压稳压器


| 电压稳压器 | 输出 | 电源 |
| --- | --- | --- |
| HP LDO | 1.1 V | HP 电源域 |
| LP LDO | 1.1 V | LP 电源域 |
| Flash LDO | 1.8 V/3.3 V | 可配置为给封装外 flash 供电 |
| VDD_MSBLDO | 1.9 V | 可配置为给封装内 PSRAM 供电 |
| V03 LDO | 0.5 ~ 2.7 V/3.3 V | 可配置为给外接器件供电 |
| V04 LDO | 0.5 ~ 2.7 V/3.3 V | 可配置为给外接器件供电 |




# 2.6.3 芯片上电和复位

芯片上电后，其电源轨需要一点时间方可稳定。之后，用于上电和复位的管脚 CHIP_PU 拉高，激活芯片。更多关于 CHIP_PU 及上电和复位时序的信息，请见图 2-3 和表 2-13。





表 2-13. 上电和复位时序参数说明


| 参数 | 说明 | 最小值(μs) |
| --- | --- | --- |
| tSTBL | CHIP_PU 管脚拉高激活芯片前，VDD_LP、VDD_IO_0、VDD_USBPHY、VDD PSU RAM_0/1、VDD_IO_4、VDD_LDO、VDD_DCDCC、VDD_IO_5、VDD_IO_6与VDD_ANA达到稳定所需的时间 | 50 |
| tRST | CHIP_PU 电平低于VIL_nRST（具体数值参考表5-4）从而复位芯片的时间 | 1000 |

# 2.7 芯片与 flash 的管脚对应关系

ESP32-P4 需要配合封装外 flash 一起使用，用于存储应用的固件和数据。ESP32-P4 支持以 SPI、Dual SPI、QuadSPI/QPI 等接口模式连接 flash，最大可支持 64 MB flash。

ESP32-P4 内部封装了十六线、1.8 V 工作电压的 PSRAM，但是 PSRAM 的管脚并没有引出芯片。

表 2-14 列出了所有 SPI 模式下芯片与 flash 的管脚对应关系。

更多关于 SPI 控制器的信息，可参考章节 4.2.2.2 SPI 控制器 (SPI)。


表 2-14. 芯片与封装外 flash 的管脚对应关系


| 管脚序号 | 管脚名称 | Single SPI | Dual SPI | Quad SPI/QPI |
| --- | --- | --- | --- | --- |
| 27 | FLASH_CS | CS# | CS# | CS# |
| 28 | FLASH_Q | DO | DO | DO |
| 29 | FLASH_WP | WP# | WP# | WP# |
| 31 | FLASH_HOLD | HOLD# | HOLD# | HOLD# |
| 32 | FLSH_CK | CLK | CLK | CLK |
| 33 | FLSHA_D | DI | DI | DI |

# 3 启动配置项

芯片在上电或硬件复位时，可以通过 Strapping 管脚和 eFuse 位配置如下启动参数，无需微处理器的参与：

• 芯片启动模式

– Strapping 管脚：GPIO35，GPIO36，GPIO37，GPIO38

• VDDO_FLASH 电压

– eFuse 位：EFUSE_0PXA_TIEH_SEL_0

• ROM 日志打印

– Strapping 管脚：GPIO36

– eFuse 位：EFUSE_UART_PRINT_CONTROL

• JTAG 信号源

– Strapping 管脚：GPIO34

– eFuse 位：EFUSE_DIS_PAD_JTAG、EFUSE_DIS_USB_JTAG 和 EFUSE_JTAG_SEL_ENABLE

上述 eFuse 位的默认值均为 0，也就是说没有烧写过。eFuse 只能烧写一次，一旦烧写为 1，便不能恢复为0。

上述 strapping 管脚如果没有连接任何电路或连接的电路处于高阻抗状态，则其默认值（即逻辑电平值）取决于管脚内部弱上拉/下拉电阻在复位时的状态。


表 3-1. Strapping 管脚默认配置


| Strapping管脚 | 默认配置 | 值 |
| --- | --- | --- |
| GPIO34 | 浮空 | - |
| GPIO35 | 弱上拉 | 1 |
| GPIO36 | 浮空 | - |
| GPIO37 | 浮空 | - |
| GPIO38 | 浮空 | - |

要改变 strapping 管脚的值，可以连接外部下拉/上拉电阻。如果 ESP32-P4 用作主机 MCU 的从设备，strapping管脚的电平也可通过主机 MCU 控制。

所有 strapping 管脚都有锁存器。芯片复位时，锁存器采样并存储相应 strapping 管脚的值，一直保持到芯片掉电或关闭。锁存器的状态无法用其他方式更改。因此，strapping 管脚的值在芯片工作时一直可读取，strapping管脚在芯片复位后作为普通 IO 管脚使用。

Strapping 管脚的信号时序需遵循表 3-2 和图 3-1 所示的 建立时间和 保持时间。


表 3-2. Strapping 管脚的时序参数说明


| 参数 | 说明 | 最小值 (ms) |
| --- | --- | --- |
| tsu | 建立时间，即拉高 CHIPPU 激活芯片前，电源轨达到稳定所需的时间 | 0 |
| tH | 保持时间，即 CHIPPU 已拉高、strapping 管脚变为普通 IO 管脚开始工作前，可读取 strapping 管脚值的时间 | 3 |

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-24/58ce4b3e-5c49-4f3a-927a-0981c6cf3d71/a4308eb392d5465f3ab52ace2b7574256fa21b7560befbcbcb8e3d9d676af1b2.jpg)






# 3.1 芯片启动模式控制

复位释放后，GPIO35~GPIO38 共同决定启动模式。详见表 3-3 芯片启动模式控制。


表 3-3. 系统启动模式控制


| 启动模式 | GPIO35 | GPIO36 | GPIO37³ | GPIO38³ |
| --- | --- | --- | --- | --- |
| SPI Boot | 1 | 任意值 | 任意值 | 任意值 |
| Joint Download Boot² | 0 | 1 | 任意值 | 任意值 |

1 加粗表示默认值和默认配置。

2 Joint Download Boot 模式下支持以下下载方式：

USB Download Boot: 

– USB-Serial-JTAG Download Boot 

USB 2.0 OTG Download Boot（只能使用 USB OTG HS 控制器以FS 速率烧录，USB OTG FS 控制器不支持设备固件升级）

UART Download Boot 

SPI Slave Download Boot 

3 有关 GPIO37 和 GPIO38 的功能，请参考 《ESP32-P4 技术参考手册》 >章节 芯片 Boot 控制。

在 SPI Boot 模式下，ROM 引导加载程序通过从 SPI flash 中读取程序来启动系统。

在 Joint Download 模式下，用户可通过 USB、UART0 或 SPI slave 接口将二进制文件下载至 flash，或将二进制文件下载至 L2MEM 并运行 L2MEM 中的程序。

除了 SPI Boot 和 Joint Download Boot 模式，ESP32-P4 还支持 SPI Download Boot 模式，详见 《ESP32-P4 技术参考手册》> 章节 芯片 Boot 控制。

# 3.2 VDDO_FLASH 电压控制

ESP32-P4 可以使用 VDDO_FLASH 给 flash 供电，VDDO_FLASH 默认输出 3.3 V 电压，可以通过烧写EFUSE_0PXA_TIEH_SEL_0 使 VDDO_FLASH 输出 1.8 V。


表 3-4. VDDO_FLASH 电压控制


| VDDO_FLASH 电源2 | EFUSE_OPXA_TIEH_SEL_0 | 电压 |
| --- | --- | --- |
| flash 稳压器 | 0 | 3.3 V |
| 2 | 1.8 V |


1 加粗表示默认值和默认配置。



2 请参考章节 2.6.2 电源管理。


# 3.3 ROM 日志打印控制

系统启动过程中，ROM 代码日志可打印至：

•（默认）UART0 和 USB 串口/JTAG 控制器

USB 串口/JTAG 控制器

• UART0 

EFUSE_UART_PRINT_CONTROL 和 GPIO36 控制 UART0 ROM 日志打印，如表 3-5 UART0 ROM 日志打印控制所示：


表 3-5. UART0 ROM 日志打印控制


| UARTO ROM 日志打印 | EFUSE_UART_PRINT_CONTROL | GPIO36 |
| --- | --- | --- |
| 使能 | 0 | 忽略 |
| 1 | 0 |
| 2 | 1 |
| 关闭 | 1 | 1 |
| 2 | 0 |
| 3 | 忽略 |


1 加粗表示默认值和默认配置。


EFUSE_DIS_USB_SERIAL_JTAG_ROM_PRINT 控制 USB 串口/JTAG 控制器 ROM 日志打印，如表 3-6 USB 串口/JTAG ROM 日志打印控制 所示。


表 3-6. USB 串口/JTAG ROM 日志打印控制


| USB串口/JTAG ROM日志打印控制 | EFUSE_DIS_USB_SERIAL_JTAG-ROM_PRINT |
| --- | --- |
| 使能 | 0 |
| 关闭 | 1 |


1 加粗表示默认值和默认配置。


# 3.4 JTAG 信号源控制

在系统启动早期阶段，GPIO34 可用于控制 JTAG 信号源。该管脚没有内部上下拉电阻，strapping 的值必须由不处于高阻抗状态的外部电路控制。

如表 3-7 JTAG 信号源控制 所示，GPIO34 与 EFUSE_DIS_PAD_JTAG、EFUSE_DIS_USB_JTAG 和EFUSE_JTAG_SEL_ENABLE 共同控制 JTAG 信号源。


表 3-7. JTAG 信号源控制


| JTAG 信号源 | EFUSE_DISPAD_JTAG | EFUSE_DISUSB_JTAG | EFUSE_JTAG_SEL_ENABLE | GPIO34 |
| --- | --- | --- | --- | --- |
| USB串口/JTAG控制器 | 0 | 0 | 0 | 忽略 |
| 0 | 0 | 1 | 1 |
| 1 | 0 | 忽略 | 忽略 |
| JTAG管脚2 | 0 | 0 | 1 | 0 |
| 0 | 1 | 忽略 | 忽略 |
| JTAG关闭 | 1 | 1 | 忽略 | 忽略 |


1 加粗表示默认值和默认配置。



2 即 MTDI、MTCK、MTMS 和 MTDO。


# 4 功能描述

# 4. 1 系统

本章节描述了芯片操作的核心部分，包括微处理器、系统 DMA、存储器组织结构、系统组件和安全功能。

# 4.1.1 微处理器和主控

本章节描述了芯片内的核心处理单元及其功能。

# 4.1.1.1 高性能处理器

ESP32-P4 搭载一个高性能 RISC-V 32 位双核处理器。

# 特性

五级流水线架构，支持 400 MHz 的时钟频率

RV32IMAFC ISA ISA (指令集架构)

• 支持 Zc 扩展 (Zcb, Zcmp, Zcmt)

支持 Zb 扩展

• 支持自定义 AI 与 DSP 扩展 (XespV)

• 支持自定义硬件循环指令 (XespLoop)

兼容 RISC-V 处理器核局部中断 (CLINT)

兼容 RISC-V 处理器核局部中断控制器 (CLIC)

支持分支预测功能 BHT，BTB 与 RAS

支持最多 3 个硬件断点/观察点

支持最多 32 个 PMP 区域和 16 个 PMA 区域

支持两个特权模式：机器模式与用户模式

用于调试的 USB/JTAG 接口

兼容 RISC-V 调试规范 v0.13

支持与 RISC-V Trace 规范 v2.0 兼容的 trace 离线调试

# 4.1.1.2 RISC-V 追踪编码器 (TRACE)

ESP32-P4 芯片中的 RISC-V 追踪编码器提供了一种从高性能 CPU 执行过程中捕获详细追踪信息的方法，以便对系统进行更深入的分析和优化。它连接到 HP CPU 的指令追踪接口，并将信息压缩成较小的数据包，然后存储在内部 SRAM 中。

# 特性

• 兼容 Efficient Trace for RISC-V v2.0（RISC-V 高效追踪规范 v2.0）

支持增量地址模式和完整地址模式

• 支持过滤器

支持通过调试触发器或过滤器报告指令地址

• 支持下列边带信号 (sideband signals) 控制追踪数据流

– 调试触发器启动或关闭编码器

– hart 暂停时，编码器在报告最后一个数据包后停止工作

– hart 复位后，编码器在报告最后一个数据包后停止工作

– FIFO 即将变满时暂停 hart

支持任意地址范围用作追踪存储器

可配置的同步模式：

– 同步计数器按包计数

– 同步计数器按周期计数

– 关闭同步计数器

支持丢包状态标识

支持丢包后自动重启

写追踪存储器时支持循环和非循环模式

具有两个中断：

– 包的大小超过配置的存储器空间时触发中断

– 丢包时触发中断

具有 128×8 位 FIFO，用于缓存数据包

支持 AHB 突发传输，突发长度可配置

# 4.1.1.3 处理器指令拓展

ESP32-P4 高性能 32 位 RISC-V 双核处理器支持标准 RV32IMAFCZc 扩展。另外，该处理器还支持自定义扩展指令集 Xhwlp 以及自定义 AI 与 DSP 扩展 Xai，Xhwlp 可降低循环体中的指令数量，Xai 可提高某些 AI 与 DSP 算法的运行效率。

# 特性

• 新增 8 个 128-bit 位宽通用寄存器

• 128-bit 位宽的向量数据操作，包括乘法、加法、减法、累加、移位、比较等

合并数据处理指令与加载/存储运算指令

• 对齐与非对齐 128-bit 带宽的向量数据加载/存储

可配置舍入与饱和模式

# 4.1.1.4 低功耗处理器

ESP32-P4 搭载一个低功耗 RISC-V 32 位单核处理器。LP CPU 可以用于在正常工作模式下协助 HP CPU，也可以用于在系统休眠时代替HP CPU来执行任务。LP CPU和LP存储器在Deep-sleep模式下仍保持工作状态。因此，开发者可以将 LP CPU 的程序存放在 LP 存储器中，使其能够在 Deep-sleep 模式下访问 LP IO、LP 外设、Real-Time 定时器。

# 特性

二级流水线架构，支持最高 40 MHz 的时钟频率

• RV32IMAC ISA (指令集架构)

支持 18 个向量中断

调试模块 (DM) 符合 RISC-V 调试规范 v0.13，支持通过行业标准的 JTAG/USB 端口连接外部调试器

硬件触发器符合 RISC-V 调试规范 v0.13，具有 2 个断点/观察点

支持核心性能指标事件

• 可唤醒 HP CPU 或向 HP CPU 发送中断

可访问 HP 存储器和 LP 存储器

可访问所有外设空间

# 4.1.2 系统 DMA

本章节描述了芯片的系统 DMA。

# 4.1.2.1 通用 DMA 控制器 (GDMA-AHB, GDMA-AXI)

通用直接存储访问 (General Direct Memory Access, GDMA) 用于在外设与存储器之间以及存储器与存储器之间提供高速数据传输。软件可以在无需 CPU 干预的情况下通过 GDMA 快速搬移数据，从而降低了 CPU 的工作负载，提高了效率。

ESP32-P4 的 GDMA 控制器有两种，分别可以直接访问 AHB 或 AXI 总线，以下简称为 GDMA-AHB 和 GDMA-AXI。

# 特性

架构:

1 GDMA-AHB：AHB 总线架构

– GDMA-AXI：AXI 总线架构，支持深度为 8 的乱序传输 (out of order) 和深度为 8 的挂起传输（outstanding传输）

数据传输以字节为单位，传输数据量可软件编程

支持任意地址和大小 (size) 访问

对齐要求：

– GDMA-AHB： 

* 描述符存储地址：字对齐

* 数据地址和长度：

· 内部存储器和外部存储器的非加密空间：无要求

· 外部存储器的加密空间：16 字节对齐

– GDMA-AXI： 

* 描述符存储地址：双字对齐

* 数据地址和长度：

· 内部存储器和外部存储器的非加密空间：无要求

· 外部存储器的加密空间：16 字节对齐

• 支持链表

GDMA-AHB 访问存储器时，支持 INCR4/8/16 突发传输

• 各有三个传输通道和三个接收通道

任一通道支持可配置的外设选择

支持通道间优先级和权重仲裁配置

支持存储搬运功能

支持链表切换中断响应机制（仅 GDMA-AXI 支持）

支持数据传输 CRC 计算功能

# 4.1.2.2 VDMA 控制器 (VDMA)

DMA（直接内存访问）是指不依赖 CPU，在存储器和外设之间完成数据搬运。ESP32-P4 上的 VDMA 控制器是一种通用 DMA，支持存储器到存储器、存储器到外设、外设到存储器的高速数据传输。VDMA 控制器以 AXI 作为总线接口，采用 AXI3 标准协议，带有两个 AXI 主机接口，支持用户动态地选择主机接口进行数据传输。

# 特性

4 个通道，每个通道都是单向的，支持源到目标的数据传输

2 个 AXI 主机接口

支持与 MIPI DSI（显示串行接口）和 ISP（图像信号处理器）的握手

• 支持存储器与存储器之间、ISP 与存储器之间、MIPI DSI 与存储器之间的 DMA 传输

• DMA 传输层次有多个级别

每个通道的传输类型、传输长度、传输大小可配置

支持单块传输

支持基于连续地址、自动重新加载、影子寄存器和链表的多块传输

支持源传输和目标传输独立配置多块传输类型

通道禁用而不丢失数据

通道暂停、恢复和中止

可配置的通道优先级仲裁

支持使用 VDMA 或外设作为流控制器

• 外设的握手接口和通道之间的映射可配置

# 4.1.2.3 2D-DMA 控制器 (2D-DMA)

2D-DMA控制器是专用于二维图像处理的DMA，在支持GDMA-AXI的全部功能基础上，增加了宏块重排(Reorder)和颜色空间转换（Color Space Convert: CSC）功能，能够更好地支持 JPEG 和 PPA 外设的数据传输需求。2D-DMA 支持存储器到存储器的传输，可以将宏块从存储器的一段地址空间搬运到另一段地址空间，并完成颜色空间转换。

# 特性

1 个 AXI 主机接口

支持首地址非对齐的数据传输

支持存储到存储、外设到存储 (RX)、以及存储到外设 (TX) 的数据传输

包含 4 个存储到外设通道，3 个外设到存储通道

支持 PPA 和 JPEG 图像编解码器外设

支持宏块重排序功能

支持颜色空间转换功能

支持通道优先级、权重配置

# 4.1.3 存储器组织结构

本章节描述了存储器布局，解释数据的存储、访问和管理方式，以实现高效的操作。

ESP32-P4 的地址映射结构如图 4-1 地址映射结构 所示。




# 4.1.3.1 系统和存储器

内部存储器

ESP32-P4 的内部存储包括：

128 KB 的 HP ROM：200 MHz，用于 HP CPU 的程序启动和内核功能调用

768 KB 的 HP L2MEM：200 MHz，用于存储 HP CPU 数据和指令

16 KB 的 LP ROM：40 MHz，用于 LP CPU 的程序启动和内核功能调用

32 KB 的 LP SRAM：40 MHz，用于存储 LP CPU 数据和指令

4 Kbit 的 eFuse：1792 位保留给用户使用，用于存储密钥或设备 ID 等信息

• 8 KB 的 HP SPM（暂存内存）: 400 MHz，用于 HP CPU 的快速访问

封装内 PSRAM

– PSRAM 大小详见章节 1 ESP32-P4 系列型号对比

– 最高时钟频率 250 MHz

– 最大支持 64 MB 存储空间

– 支持 XTS-AES 硬件加解密，保护 PSRAM 中的程序和数据

– 通过高速缓存，可以以 64 KB 块映射到 64 MB 的指令空间或数据空间，支持 8 位、16 位、32 位和128 位读写

PSRAM 的最大理论带宽计算应遵循如下公式：

```txt
Max theoretical bandwidth (PSRAM) = line_num × edge_mode × PSRAM_max_freq 
```

其中：

• line_num 是 PSRAM 的数据线数量。

• edge_mode 是 PSRAM 的边沿采样模式，1 为单边沿采样，2 为上边沿采样。

PSRAM_max_freq 是 PSRAM 的最高运行时钟频率。

以当前封装内 PSRAM 参数为例，其理论最大带宽为：16 × 2 × 250 MHz = 8 Gbit/s。

# 外部存储器

ESP32-P4 支持通过 SPI、Dual SPI、Quad SPI、QPI 等接口在芯片封装外连接存储器。最高时钟频率为 120MHz。

外部 flash 可以映射到 CPU 的指令空间、只读数据空间。外部 flash 最大支持容量为 64 MB。ESP32-P4 支持基于 XTS-AES 的硬件加解密功能，从而保护开发者 flash 中的程序和数据安全。

通过高速缓存，ESP32-P4 一次最多可以同时有：

• 外部 flash 以 64 KB 的块映射到 64 MB 的指令空间。

外部 flash 也可以以 64 KB 的块映射到 64 MB 只读数据空间，支持 8 位、16 位、32 位和 128 位读取。

说明：

芯片启动完成后，软件可以自定义外部 flash 到 CPU 地址空间的映射。

# 4.1.3.2 eFuse 控制器 (eFuse)

ESP32-P4 中有一块 4096 位的 eFuse 存储器用于存储参数内容和用户数据，参数内容包括一些硬件模块的控制参数、系统数据参数以及加解密模块使用的密钥等。eFuse 存储器的各个位一旦被烧写为 1，则不能再恢复为0。

# 特性

4096 位一次性可编程存储（最多有 1792 个保留位供用户使用）

烧写保护可配置

读取保护可配置

使用多种硬件编码方式保护参数内容

# 4.1.3.3 Cache

ESP32-P4 采用两级 cache 结构。

# 特性

• L1 指令 cache 的大小为 16 KB，块大小为 64 B，四路组相联

• L1 数据 cache 的大小为 64 KB，块大小为 64 B，两路组相联，支持 write-through 和 write-back 两种写策略

• l2 cache 的大小为 128 KB/256 KB/512 KB，块大小为 64 B/128 B，八路组相联

• 支持 cacheable 和 non-cacheable 访问

• 支持 pre-load 功能

支持 lock 功能

• 支持关键字优先 (critical word first) 和提前重启 (early restart)

# 4.1.4 系统组件

本章节描述了对系统的整体功能和控制起到重要作用的组件。

# 4.1.4.1 GPIO 交换矩阵和 IO MUX

ESP32-P4 共有 55 个 GPIO 管脚，其中包括 16 个低功耗 (LP) GPIO 管脚和 39 个高性能 (HP) GPIO 管脚。每个管脚都可用作一个通用 IO，或连接一个内部的外设信号。

利用 HP GPIO 交换矩阵和 HP IO MUX，可配置 HP 外设模块的输入信号来源于任何的 GPIO 管脚，并且 HP外设模块的输出信号也可连接到任意 GPIO 管脚。

利用 LP GPIO 交换矩阵和 LP IO MUX，可配置 LP 外设模块的输入信号来源于任何的 LP GPIO 管脚，并且LP 外设模块的输出信号也可连接到任意 LP GPIO 管脚。

这些模块共同组成了芯片的 GPIO 控制。上述 55 个 GPIO 管脚的编号为：GPIO0~GPIO54。

• GPIO 管脚 0 ~ 15 为 LP GPIO 管脚，可由 HP 或 LP 外设使用。

GPIO 管脚 16~54 为 HP GPIO 管脚，只能由 HP 外设使用。

# 特性

# HP GPIO 交换矩阵具有以下特性：

HP 外设输入输出信号和 GPIO 管脚之间的全交换矩阵

222 个 HP 外设输入信号可以选择任意一个 GPIO 管脚的输入信号

每个 GPIO 管脚的输出信号可以来自 232 个 HP 外设输出信号的任意一个

HP 外设输入信号经 GPIO SYNC 模块同步至 HP IO MUX 运行时钟

支持 GPIO 滤波器对输入信号进行滤波

支持毛刺滤波器对输入信号进行二次滤波

• 支持 Sigma Delta 调制输出 (SDM)

支持 GPIO 简单输入输出

支持 HP GPIO 唤醒

# HP IO MUX 具有以下特性：

• 控制 55 个 GPIO (GPIO0~GPIO54) 供 HP 外设使用

为每个 GPIO 管脚提供一个寄存器，用于控制管脚的输入/输出、上拉/下拉、驱动强度、功能选择等配置

支持高频信号如 SPI、EMAC 等直接通过 HP IO MUX 输入和输出外设，实现更好的高频数字特性

# LP GPIO 交换矩阵具有如下特性：

LP 外设输入输出信号和 LP GPIO 管脚之间的全交换矩阵

• 14 个 LP 外设输入信号可以选择任意一个 LP GPIO 管脚的输入信号

每个 LP GPIO 管脚的输出信号可以来自 14 个 LP 外设输出信号的任意一个

支持 GPIO 滤波器对输入信号进行滤波

支持 GPIO 简单输入输出

• 支持 LP GPIO 唤醒

# LP IO MUX 具有如下特性：

• 16 个 LP GPIO 管脚 (GPIO0~GPIO15) 供 LP 外设使用

为每个 LP GPIO 管脚提供一个寄存器，用于控制管脚的输入/输出、上拉/下拉、驱动强度、功能选择、IOMUX 选择等配置

# 4.1.4.2 复位

ESP32-P4 提供四种级别的复位方式，分别是 CPU 复位 (CPU reset)、内核复位 (Core reset)、系统复位 (Systemreset) 和芯片复位 (Chip reset)。除芯片复位外，其他复位方式不影响片上内存存储的数据。

支持四种复位等级：

– CPU 复位：复位 CPU 核，HP CPU0、HP CPU1、LP CPU 各有一套独立复位。其中：

* HP CPU0 上电后会自动释放复位；

HP CPU1 上电后默认处于复位状态，需要手动释放复位；

* LP CPU 上电后处于复位状态，需要配置 PMU 释放。

– 内核复位：包括 HP 以及 LP 的内核复位，复位除 LP AON 以外的其他数字系统。HP 内核复位包括 HPCPU0、HP CPU1、HP 外设、HP GPIO 等，LP 内核复位包括 LP CPU、LP 外设等；

– 系统复位：复位包括低功耗系统在内的整个数字系统；

– 芯片复位：复位整个芯片。

支持软件复位和硬件复位：

– 软件复位：CPU 配置相关寄存器可触发软件复位；

– 硬件复位：硬件复位直接由硬件电路触发。

# 4.1.4.3 时钟

ESP32-P4 的时钟主要来源于振荡器（oscillator, OSC，包括 RC 振荡电路）、晶振 (XTAL) 和 PLL 时钟生成电路。上述时钟源产生的时钟经时钟分频器或时钟选择器等时钟模块的处理，使得大部分功能模块可以根据不同功耗和性能需求来获取及选择对应频率的工作时钟。

ESP32-P4 的时钟根据频率不同，可分为：

高性能时钟，主要为 HP CPU0/1 和 HP 数字外设提供工作时钟

– CPLL_CLK：400 MHz 内部 PLL 时钟（参考时钟是 XTAL_CLK）

– MPLL_CLK：500 MHz 内部 PLL 时钟（参考时钟是 XTAL_CLK）

– SPLL_CLK：480 MHz 内部 PLL 时钟（参考时钟是 XTAL_CLK）

低功耗时钟，主要为低功耗系统以及部分处于低功耗模式的外设提供工作时钟

– XTAL32K_CLK：32 kHz 外部晶振时钟

– RC_SLOW_CLK：内置慢速 RC 振荡器，频率可调节（通常为 150 kHz）

– OSC_SLOW_CLK：外置低速时钟，通常频率为 32 kHz

– XTAL_CLK：40 MHz 外部晶振时钟

– RC_FAST_CLK：内置快速 RC 振荡器时钟，频率可调节（通常为 20 MHz）

– PLL_LP_CLK：内部 PLL 时钟，通常为 8 MHz，参考时钟可选为 XTAL32K_CLK

# 4.1.4.4 中断矩阵

ESP32-P4 芯片的中断矩阵用于将外设和事件生成的中断请求映射到 CPU 中断。

# 特性

接收 126 个外部中断源作为输入

生成 32 个 HP CPU0 的外部中断和 32 个 HP CPU1 的外部中断作为输出

支持查询外部中断源当前的中断状态

支持将多个中断源映射到单个 HP CPU0 中断或 HP CPU1 中断（即共享中断）

# 4.1.4.5 事件任务矩阵

事件任务矩阵 (ETM) 外设包含 50 个可配置通道。每个通道可以将任意指定外设的事件映射到任意指定外设的任务，从而触发外设执行指定任务，无需 CPU 干预。

# 特性

支持从多个外设接收多种事件

支持为多个外设生成多种任务

拥有 50 个可独立配置的 ETM 通道

• 每个通道接收到的事件可以是所有事件中的任意一个，每个通道接收到的事件可以映射到任意的任务上输出

• 每个 ETM 通道都可以独立使能。当通道未使能时，它不会响应所配置的事件，也不会生成要映射到的任务

支持查看每个事件和任务的触发状态

• 能够产生事件、接收任务的外设有：GPIO、LED PWM、通用定时器、RTC 定时器、系统定时器、MCPWM、温度传感器、ADC、I2S、LP CPU、GDMA-AHB、GDMA-AXI、2D DMA 和 PMU

# 4.1.4.6 低功耗管理

ESP32-P4 采用了先进的电源管理技术，可以在不同的功耗模式之间切换。ESP32-P4 支持的功耗模式包括：

• Active 模式：CPU 处于工作状态，所有外设均可工作。

Light-sleep 模式：CPU 暂停运行。任何唤醒事件（主机、RTC 定时器或外部中断）都会唤醒芯片。用户可将 CPU（不含 L2MEM）以及大部分外设可根据实际需求配置（见 ESP32-P4 功能框图）为关闭，进一步降低功耗。

Deep-sleep 模式：CPU（含 L2MEM）和大部分外设（见 ESP32-P4 功能框图）都会掉电。低功耗存储器(LP Memory) 处于工作状态，低功耗系统的部分外设可根据需求关闭。

# 4.1.4.7 系统定时器

ESP32-P4 芯片内置 52 位系统定时器。该定时器可用于生成操作系统所需的滴答定时中断，也可以用作普通的定时器生成周期或单次延时中断。

# 特性

• 集成两个 52 位计数器和三个 52 位比较器

支持软件访问由 APB_CLK 时钟驱动的寄存器

• 支持 CNT_CLK 时钟计数，两次计数周期的平均频率为 16 MHz

配置 XTAL_CLK (40 MHz) 作为 CNT_CLK 时钟源

• 支持 52 位报警值 (t) 和 26 位报警周期 (δt)

支持两种报警模式：

– 单次报警模式：根据设定的目标报警值 (t)，生成一次性报警

1 周期报警模式：根据设定的报警周期 (δt)，生成周期性报警

• 支持根据设置的报警值 (t) 或报警周期 (δt)，通过三个比较器生成三个独立中断

支持软件配置基准计数值。例如，支持从 Light-sleep 唤醒之后，系统定时器通过软件加载 RTC 定时器记录的睡眠时间，并进行补偿

CPU 处于停止状态或处于在线调试状态时，系统定时器可选择停止运行或继续运行

支持事件任务矩阵 (ETM) 事件报警

# 4.1.4.8 定时器组 (TIMG)

ESP32-P4 包含两个定时器组，每个定时器组有两个通用定时器和一个主系统看门狗定时器 (MWDT)。通用定时器基于 16 位预分频器和 54 位可自动重新加载的可逆计数器。

# 特性

• 54 位时基计数器，可配置成递增或递减

三个时钟源：PLL_F80M_CLK 或 XTAL_CLK 或 RC_FAST_CLK 时钟

16 位时钟预分频器，分频系数为 2 到 65536

可读取时基计数器的实时值

暂停和恢复时基计数器

可配置的报警产生机制

计数器值重新加载——报警时自动重新加载或软件控制的即时重新加载

• 时钟频率计算——基于晶振时钟计算导入 TIMG0 的被测时钟频率

电平触发中断

支持多个 ETM 任务和事件

# 4.1.4.9 看门狗定时器 (WDT)

ESP32-P4 中有三个数字看门狗定时器：两个定时器组中各有一个主系统看门狗定时器，缩写为 MWDT，LP 系统中有一个 RTC 看门狗定时器，缩写为 RWDT。

在 SPI Boot 模式下，RWDT 和定时器组 0 的 MWDT 会默认使能，以检测引导过程中发生的错误，并恢复运行。

ESP32-P4中还有一个模拟看门狗定时器——超级看门狗(SWD)。超级看门狗是模拟域的超低功耗电路，可以防止系统在数字电路异常状态下运行，并在必要时复位系统。

# 特性

四个阶段，每个阶段都可配置超时时间和超时动作

超时动作

– MWDT：中断、HP CPU 复位、HP 内核复位

1 RWDT：中断、HP CPU 复位、HP 内核复位、系统复位

阶段 0 flash 启动保护（SPI Boot 模式）：

– MWDT0：超时触发 HP 内核复位

– RWDT：超时触发系统复位

写保护，使能时寄存器仅可读取

32 位超时计数器

时钟源：

– MWDT：PLL_F80M_CLK、RC_FAST_CLK 或 XTAL_CLK

– RWDT：LP_DYN_SLOW_CLK 

# 4.1.4.10 实时时钟定时器

RTC Timer 是实现 ESP32-P4 低功耗管理的一个重要模块。RTC Timer 是一个 48 位的可读计时器，主要作用是在低功耗模式下，当 HP 系统中的定时器外设不可用时，继续为系统提供定时器服务。同时还支持配置定时器中断、记录系统中特定事件发生的时刻。

# 特性

• 48 位的计时器

触发特定事件时可记录事件发生的时刻，支持的特定事件有：

– HP 系统复位

– CPU 进入 stall 状态

– CPU 退出 stall 状态

– 晶振时钟开启

– 晶振时钟关闭

• 通过配置寄存器触发 RTC Timer 记录当前时间

支持缓存最近两次特定事件的发生的时间

支持在目标时刻产生中断，目标时刻可配置，可同时配置两个目标时刻

除 LP 系统上电复位外的其余任何复位/睡眠均不会使 RTC Timer 停止或复位

# 4.1.4.11 权限控制 (PMS)

ESP32-P4 集成 APM (Access Permission Management) 模块实现访问的权限管理。

# 特性

• 最多可为 DMA 主机配置 32 组有效地址区间

支持独立控制 CPU 每种模式下对内部存储器、外部存储器以及外设寄存器的访问权限

. 支持中断功能

• 支持异常信息记录功能

# 4.1.4.12 系统寄存器

ESP32-P4 芯片中的系统寄存器用于配置多种辅助芯片功能。

# 特性

控制外部内存加密和解密

控制 HP/LP 核心调试

控制总线超时保护

# 4.1.4.13 辅助调试

辅助调试可以帮助在软件调试过程中定位错误和问题，提供各种监视能力和日志记录功能，以帮助高效地识别和解决软件错误。

# 特性

• 读写监测：监测一个高性能双核处理器（High-Performance CPU, HP CPU0 和 HP CPU1）总线是否在限定的存储器地址范围内进行读写操作，若在该地址范围内发生读写操作则触发中断。

• 栈指针 (SP) 监测：监测栈指针是否超出限定的范围，若超出范围则产生中断。

• 程序计数器 (PC) 记录：记录 PC，可以获得上一次 HP CPU0 或 HP CPU1 复位时的 PC 值。

总线访问记录：记录总线访问信息，当 HP CPU0、HP CPU1 或 DMA 写了某个特殊值时，会记录此次写操作的总线类型、地址和 PC 值（仅记录 HP CPU0 或 HP CPU1 写操作的 PC），并将这些信息记录到 HPL2MEM 中。

# 4.1.4.14 LP 信箱控制器

ESP32-P4 包含一个 LP 信箱控制器模块，旨在通过硬件机制以实现 LP CPU 和 HP CUP0/1 之间高效的核间通信。LP 信箱控制器模块中包含 16 个 32 位信息寄存器可供 LP CPU 和 HP CPU0/1 存储并传递信息，并通过中断机制实现 LP CPU 和 HP CPU0/1 之间的核间通信。

# 特性

• 支持多达 16 个 32 位信息寄存器用于核间通信

• 支持 LP CPU 外部中断信号

• 支持 HP CPU0/1 外部中断信号

# 4.1.4.15 欠压检测器

ESP32-P4 的欠压检测器可以检查管脚 VDD_ANA，VDD_BAT 的电压，在电压快速下落至预设阈值（默认为 2.4V）以下时发出触发信号，并进行相应处理，从而关闭部分耗电模块（主要是 flash 模块），为数字模块争取更多时间，用以保存、转移重要数据。

# 特性

• 支持 VDD_ANA 与 VDD_BAT 管脚欠压检测

支持两种检测模式

– 模式 0：当欠压计数器达到设定的阈值后触发中断，并根据配置选择复位方式

– 模式 1：欠压发生后直接触发系统复位

支持监控阈值与噪声过滤的配置

支持欠压后的复位等级选择

# 4.1.5 加密和安全组件

本章节描述了集成在芯片中用于保护数据和操作的安全功能。

# 4.1.5.1 AES 加速器 (AES)

ESP32-P4 内置 AES（高级加密标准）硬件加速器可使用 AES 算法，完成数据的加解密运算，具有 typical AES和 DMA-AES 两种工作模式。整体而言，相比基于纯软件的 AES 运算，AES 硬件加速器能够极大地提高运算速度。另外，ESP32-P4 AES 加速器包含可配置的抗旁路攻击 (anti-DPA) 功能，提供了高安全性。

# 特性

Typical AES 工作模式

– AES-128/AES-256 加解密运算，符合标准 NIST FIPS 197

DMA-AES 工作模式

– AES-128/AES-256 加解密运算，符合标准 NIST FIPS 197

– 块（加密）模式，符合标准 NIST SP 800-38A

* ECB (Electronic Codebook) 

* CBC (Cipher Block Chaining) 

* OFB (Output Feedback) 

* CTR (Counter) 

* CFB8 (8-bit Cipher Feedback) 

* CFB128 (128-bit Cipher Feedback) 

– 伽罗瓦/计数器模式 (Galois/Counter Mode, GCM)

– 中断发生

可配置的抗旁路攻击 (anti-DPA) 功能

# 4.1.5.2 ECC 加速器 (ECC)

椭圆曲线密码学 (Elliptic Curve Cryptography) 是一种基于椭圆曲线数学的公开密钥加密演算法，其优势在于相对于 RSA 算法，使用较小长度的密钥就能够提供相当等级的加密安全性。

ESP32-P4 ECC硬件加速器支持对于可选曲线的多种基础运算，用以实现对ECC基本运算、衍生算法（如ECDSA等算法）的加速。

# 特性

支持三种可选 ECC 曲线，即 FIPS 186-5 中定义的 P-192、P-256 和 P-384

提供两种可选坐标系，即仿射坐标系和 Jacobian 坐标系

提供多种可选点运算，包含点加、点乘和点验证

提供基于曲线阶数或模数的多种可选模运算，包含模加、模减、模乘、模除

提供计算完成的中断和中断控制

支持安全工作模式，进行固定时间的点乘运算

# 4.1.5.3 HMAC 加速器 (HMAC)

HMAC 加速器 (HMAC) 模块用于使用 SHA-256 哈希算法和 RFC 2104 中描述的密钥计算信息认证码 (MAC)。它提供了硬件支持的 HMAC 计算，显著降低了软件复杂性，提高了性能。

# 特性

使用标准 HMAC-SHA-256 算法

• 仅支持可配的硬件外设访问 HMAC 计算的 hash 结果（下行模式）

兼容挑战-应答身份验证算法

支持生成数字签名外设所需的密钥（下行模式）

重启软禁用的 JTAG（下行模式）

# 4.1.5.4 RSA 加速器 (RSA)

RSA 加速器可为多种运用于“RSA 非对称式加密演算法”的高精度计算提供硬件支持，能够极大地降低此类运算的运行时间和软件复杂度。与纯软件 RSA 算法相比，硬件 RSA 加速器的运算速度更快。RSA 加速器还支持多种“运算子长度”，具有很高的灵活性。

# 特性

大数模幂运算（支持两个加速选项）

大数模乘运算，最大可达 4096 位

大数乘法运算，运算子最大可达 2048 位

多种运算子长度

• 支持在运算完成后触发中断

# 4.1.5.5 SHA 加速器 (SHA)

SHA（安全哈希算法）硬件加速器可完成 SHA 运算，具有典型 SHA 和 DMA-SHA 两种工作模式。相比基于纯软件的 SHA 运算，SHA 硬件加速器能够极大地提高运算速度。

# 特性

支持 FIPS PUB 180-4 中的以下运算标准

– SHA-1 运算

– SHA-224 运算

– SHA-256 运算

– SHA-384 运算

– SHA-512 运算

– SHA-512/224 运算

– SHA-512/256 运算

– SHA-512/t 运算

支持 SM3 密码杂凑算法

提供两种工作模式

– 典型 SHA 工作模式

– DMA-SHA 工作模式

• 允许插入 (interleaved) 功能（仅限典型 SHA 工作模式）

• 允许中断功能（仅限 DMA-SHA 工作模式）

# 4.1.5.6 RSA 数字签名外设 (RSA_DS)

数字签名技术使用密码学算法，用于验证消息的真实性和完整性。该技术也可用于向服务器验证设备身份，或验证消息是否经过篡改。

ESP32-P4 包含 RSA 数字签名外设 (RSA_DS)，可提供硬件加速，高效生成基于 RSA 的数字签名。RSA_DS 外设使用 RSA_DS_KEY（由 HMAC 生成或由密钥管理器部署）解密预先加密的参数，计算出签名。上述过程都发生在硬件层面，因此在计算过程中，不论是解密 RSA 参数的密钥，HMAC 密钥导出函数的输入/输出密钥，还是由密钥管理器部署的密钥，都对用户不可见。

# 特性

• 支持长度最大为 4096 位的 RSA 数字签名密钥

支持仅限 RSA_DS 外设读取的加密私钥数据

• 支持 SHA-256 摘要，用于保护私钥数据免遭攻击者篡改

# 4.1.5.7 ECDSA 数字签名外设 (ECDSA_DS)

在密码学中，椭圆曲线数字签名算法 (ECDSA) 是使用椭圆曲线密码对数字签名算法 (DSA) 的模拟。

ESP32-P4 的 ECDSA 数字签名外设 (ECDSA_DS) 可高效计算 ECDSA 签名，同时确保签名过程的保密性，防止信息泄露。它在提供强大安全保障的同时，不影响运算性能，可用于高速加密运算，保护用户数据安全。

# 特性

. 支持数字签名的生成和验证

支持三种 NIST 椭圆曲线，分别是 P-192、P-256 和 P-384（具体定义见 FIPS 186-5 规范）

支持多种哈希算法，包括 SHA-224、SHA-256、SHA-384、SHA-512、SHA-512/224、SHA-512/256（具体定义见 FIPS PUB 180-4 规范）和国密 SM3 算法（具体定义见 SM3 密码杂凑算法）

支持国密 SM2 算法（具体定义见 SM2 椭圆曲线公钥密码算法）

提供高安全性特性

– 拥有不同工作状态下的动态访问权限控制，防止一切中间数据泄漏而导致的密钥泄露

– 签名/验证为固定时长操作，抵抗旁路攻击

# 4.1.5.8 片外存储器加密与解密 (XTS_AES)

ESP32-P4 芯片集成了片外存储器加密与解密模块，使用 IEEE Std 1619-2007 指定的 XTS-AES 标准算法，为用户存放在片外存储器（flash 和 RAM）的应用代码和数据提供了安全保障。用户可以将专有固件、敏感的用户数据（如用来访问私有网络的证书）存放在片外 flash 中，或将一般数据存放在片外 RAM 中。

# 特性

使用通用 XTS-AES 算法，符合 IEEE Std 1619-2007

支持手动加密，需要软件参与

支持高速自动加密，无需软件参与

支持高速自动解密，无需软件参与

由寄存器配置、eFuse 参数、启动 (boot) 模式共同决定开启/关闭加解密功能

支持可配置的抗旁路攻击 (anti-DPA) 功能

flash 和 PSRAM 使用各自独立的密钥

# 4.1.5.9 随机数发生器 (RNG)

ESP32-P4 内置一个真随机数发生器，其生成的 32 位随机数可作为加密等操作的基础。

ESP32-P4 的真随机数发生器通过物理过程而非算法生成真随机数，所有生成的随机数在特定范围内出现的概率完全一样。

# 特性

随机数发生器的熵源

– 来自 SAR ADC 的热噪声

– 异步时钟

– 环形振荡器 (BUF_CHAIN)

# 4.1.5.10 密钥管理器

ESP32-P4 密钥管理器可作为系统的安全核心，以实现高安全性的密钥存储和部署。密钥管理器利用每一块芯片独有的物理不可复制特性 (PUF)，生成每一块芯片独有的硬件唯一密钥 (HUK)，以此作为一块芯片的信任根。HUK 在每次芯片上电时自动生成，在芯片掉电后消失。密钥管理器以这种方式保证密钥存储和部署的安全。

ESP32-P4 的密钥管理器，将密钥信息（非明文，用于恢复密钥的信息）存储在外部储存器中，能够实现无限制数量的密钥存储、实现动态密钥切换等灵活密钥管理功能。

# 特性

# HUK 生成器具有以下特性：

HUK 生成模式：

– 生成新 HUK 及其对应的 HUK 恢复信息

• HUK 恢复模式：

– 使用 HUK 恢复信息来恢复 HUK

• HUK 恢复错误提示

HUK 风险等级提示

# 密钥管理器具有以下特性：

密钥数量无限

指定私钥部署（AES 部署模式）

– 用户可指定密钥的值

协商私钥部署（ECDH0 部署模式）

– 最高安全模式，无需担心外部渠道的数据泄露

– 获取私钥需初始化芯片

– 密钥值为芯片与用户协商所得

协商私钥部署（ECDH1 部署模式）

– 利用辅助密钥部署协商私钥

– 获取私钥无需启动芯片

随机密钥部署（随机部署模式）

– 部署硬件生成的随机密钥，无人知道其确切值

• 私钥恢复部署

– 输入部署时生成的密钥信息可恢复完全相同的密钥

密钥信息导出

– 为同一个密钥每次生成不同的密钥信息

# 4.2 外设

本章节介绍了芯片上的外设接口，包括扩展芯片功能的通信接口和片上传感器。

# 4.2.1 图像处理

本章节介绍了图像与声音处理的外设。

# 4.2.1.1 JPEG 图像编解码器

ESP32-P4 的 JPEG 图像编解码器是一种基于 JPEG 基线标准的图像编解码器，可以对图像进行压缩（编码）和解压缩（解码），从而降低传输图像所需的带宽或存储图像所需的空间，可以处理高分辨率的图像。

# 特性

JPEG 图像编解码器作为编码器使用时，具有以下特性：

• 使用离散余弦变换算法

使用范式哈夫曼编码

原始输入图像格式支持 RGB888、RGB565、YUV444、YUV422、YUV420 和 GRAY

支持将 RGB888、RGB565、YUV444 图像进行转换（如有需要）并压缩为 YUV444、YUV422 或 YUV420格式，支持对 YUV422 图像进行转换（如有需要）并压缩为 YUV422 或 YUV420 格式（压缩功能仅适用于YUV444、YUV422 和 YUV420 格式）

支持 4 个 8 位或 16 位精度的可配置量化系数表

• 性能：

– 静态图像压缩最大支持 4K 分辨率

– 动态图像压缩最大支持 1080P@40fps，720P@70fps（不包括包头编码时间）

可自动填充零字节

可自动添加 EOI 标记

JPEG 图像编解码器作为解码器使用时，具有以下特性：

• 使用反离散余弦变换算法

使用哈夫曼解码

• 支持 YUV444、YUV422、YUV420、GRAY 图像格式的压缩码流解码

支持 4 个 8 位或 16 位精度的可配置量化系数表

支持 2 个 DC 和 2 个 AC 哈夫曼表

• 支持任意分辨率的图像解码，但输出的解码图像分辨率不同于输入图像格式：

– YUV444、GRAY：输出的解码图像水平和垂直分辨率均为 8 的倍数，即 150×150 的图像输出分辨率为 152×152

– YUV422：输出的解码图像水平分辨率为 16 的倍数，垂直分辨率为 8 的倍数，即 150×150 的图像输出分辨率为 160×152

– YUV420：输出的解码图像水平和垂直分辨率均为 16 的倍数，即 150×150 的图像输出分辨率为 160×160

性能：

– 静态图像解码最大支持 4K 分辨率

– 动态图像解码最大支持 1080P@40fps，720P@70fps（不包括包头解析时间）

# 管脚分配

JPEG 编/解码器无需直接与 IO 进行交互，因此无需分配管脚。

# 4.2.1.2 图像信号处理器 (ISP)

ESP32-P4 带有一个图像信号处理器 (ISP)，该模块是一个由多种图像处理算法所组成的流水线。

# 特性

最大分辨率支持 1920 x 1080

支持三个数据输入源：MIPI-CSI、DVP、AXI-DMAC

对于 MIPI-CSI 输入，支持像素下采样以及字节序调整

输入格式支持：RAW8、RAW10、RAW12

• 输出格式支持：RAW8、RGB888、RGB565、YUV422、YUV420

流水线功能：

– 黑电平矫正 (BLC)

– 坏点矫正 (DPC)

– 拜耳域降噪 (BF)

– 镜头阴影矫正 (LSC)

– 去马赛克

– 白平衡增益 (WBG)

– 颜色矫正矩阵 (CCM)

– gamma 矫正

– RGB 转 YUV (RGB2YUV)

– 锐化 (sharpen)

– 亮度、对比度、饱和度、色相调节 (COLOR)

– YUV 范围调整

– YUV 转 RGB (YUV2RGB)

– 裁剪 (CROP)

– 自动曝光统计 (AE)

– 自动对焦统计 (AF)

– 自动白平衡统计 (AWB)

– 直方图统计 (HIST)

# 管脚分配

图像信号处理器的 CAM 接口通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.1.3 像素处理加速器 (PPA)

ESP32-P4带有一个像素处理加速器(PPA)，PPA主要包括两大功能模块：旋转－缩放－镜像(SRM)和图层叠加(BLEND)。

# 特性

SRM 支持图像块旋转、缩放、镜像：

– 输入格式支持 ARGB8888、RGB888、RGB565、YUV422、YUV420、GRAY

– 输出格式支持 ARGB8888、RGB888、RGB565、YUV422、YUV420、GRAY

– 逆时针旋转角度支持 $0 ^ { \circ }$ 、 $9 0 ^ { \circ }$ 、 ${ 1 8 0 ^ { \circ } }$ 、270°

– 水平、垂直方向独立缩放支持 8 位整数及 4 位小数

– 水平、垂直方向镜像

BLEND 支持两个相同尺寸的图层叠加以及输出特定像素的填充图像：

– 前景输入格式支持 ARGB8888、RGB888、RGB565、L4、L8、A4、A8

– 背景输入格式支持 ARGB8888、RGB888、RGB565、YUV422、YUV420、GRAY、L4、L8

– 输出格式支持 ARGB8888、RGB888、RGB565、YUV422、YUV420、GRAY

– 基于 Alpha 通道的图层叠加，若图层没有 Alpha 通道，可通过寄存器配置提供

– 前景和背景支持通过设置 color-key 范围实现特殊颜色抠图

# 管脚分配

像素处理加速器无需直接与 IO 进行交互，因此无需分配管脚。

# 4.2.1.4 LCD 与 Camera 控制器 (LCD_CAM)

ESP32-P4 的 LCD_CAM 控制器包含一个独立的 LCD 控制模块和 Camera（摄像头）控制模块，可以外接 LCD 和摄像头设备，功能灵活多样。

# 特性

支持以下工作模式：

– LCD 主机发送模式

– Camera 从机接收模式

– Camera 主机接收模式

支持同时外接 LCD 和摄像头设备

当外接 LCD 设备时，支持：

– 8/16/24 位并行输出模式

– RGB、MOTO6800、I8080 多种 LCD 模式

– LCD 数据可由 GDMA 取自内部或外部存储器

当外接摄像头设备（即 DVP 图像传感器）时，支持：

– 8/16 位并行输入模式

– 视频数据可由 GDMA 存入内部或外部存储器

• 支持 LCD_CAM 接口中断

# 管脚分配

Camera-LCD 控制器的 CAM 和 LCD 接口通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.1.5 H264 编码器

ESP32-P4 包含一个 baseline H264 视频编码器，它用于实时压缩视频序列，可以显著减少数据总量，同时视频质量损失最小。

# 特性

支持 RGB888、RGB565、YUV444、YUV422、YUV420、GRAY 逐行视频输入，最大编码性能为 1080p@30fps（编码格式为 YUV420）

支持 I 帧和 P 帧

支持两种工作模式：GOP 模式和双码流模式（在双码流工作模式下，要编码的两个视频图像序列总带宽不超过 1080p@30fps）

支持帧内亮度宏块 4 x 4 分割和 16 x 16 分割

支持帧内亮度宏块 4 x 4 分割的所有 9 种预测模式，16 x 16 分割的所有 4 种预测模式

支持帧内色度宏块的所有 4 种预测模式

支持帧间预测宏块所有的分割模式：4 x 4，4 x 8，8 x 4，8 x 8，8 x 16，16 x 8，16 x 16

支持 1/2 和 1/4 像素精度运动估计

• 支持帧间预测水平方向运动搜索范围 [–29.75, +16.75]，垂直方向搜索范围 [–13.75, +13.75]

支持去块滤波的打开和关闭

支持上下文自适应变长编码（CAVLC）

支持 P-skip 块

P 切片 (slice) 支持 I 宏块

支持亮度和色度分量量化结果缩减操作

支持定 QP 以及宏块级码率控制

支持 MV 合并功能，可以将各个宏块的 MV 输出到存储器中

支持感兴趣区域 (ROI)，最多可以配置 8 个任意位置的矩形 ROI 区域（允许重叠，固定优先级），每个 ROI区域可以为定 QP 或 QP 偏移，非 ROI 区域可以指定 QP 的偏移

# 管脚分配

H264 编码器无需直接与 IO 进行交互，因此无需分配管脚。

# 4.2.1.6 MIPI 相机串行接口

ESP32-P4 带有一个 MIPI CSI 接口，用于连接 MIPI 接口的摄像头。

# 特性

• 符合 MIPI CSI-2 协议

• 使用 DPHY v1.1 版本

• 2-lane x 1.5 Gbps 

输入格式支持 RGB888、RGB666、RGB565、YUV422、YUV420、RAW8、RAW10、RAW12

# 管脚分配

MIPI 相机串行接口使用专用数字管脚，管脚序号为 42~48。

# 4.2.1.7 MIPI 显示串行接口

ESP32-P4 带有一个 MIPI DSI 接口，用于连接 MIPI 接口的显示屏。

# 特性

• 符合 MIPI DSI 协议

使用 DPHY v1.1 版本

• 2-lane x 1.5 Gbps 

输入格式支持 RGB888、RGB666、RGB565、YUV422、YUV420、GRAY

输出格式支持 RGB888、RGB666、RGB565

使用 video mode 输出视频流

支持输出固定图像 pattern

# 管脚分配

MIPI 显示串行接口使用专用数字管脚，管脚序号为 34~40。

# 4.2.2 通讯接口

本章节介绍了芯片与外部设备和网络进行通信和交互的接口。

# 4.2.2.1 UART 控制器 (UART)

ESP32-P4 芯片中共有六个 UART 控制器，包含五个在主系统中的 UART 和一个低功耗 LP UART。

# 特性


表 4-1. UART 和 LP UART 特性区分


| UART特性 | LP UART特性 |
| --- | --- |
| 可编程收发波特率,最大为5MBaud |
| 每个UART的发送FIFO和接收FIFO共用260x8bit存储空间 | LP UART的发送FIFO和接收FIFO共用20x8bit存储空间 |
| 全双工异步通信 |
| 数据位(5到8位) |
| 停止位(1、1.5或2位) |
| 奇偶校验位 |
| AT_CMD特殊字符检测 |
| RS485协议 | - |
| IrDA协议 | - |
| GDMA高速数据通信 | - |
| 接收超时 |
| UART唤醒模式 |
| 软件流控和硬件流控 |
| 三个可分频的时钟源:1.XTAL_CLK2.RC_FAST_CLK3.PLL_F8OM_CLK | 三个可分频的时钟源:1.RC_FAST_CLK2.XTAL_DIV_CLK3.PLL_F8M_CLK |

# 管脚分配

UART0~UART4 接口通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。默认情况下，UART0 接口连接发送和接收信号（UART0_TXD_PAD 和 UART0_RXD_PAD）的管脚通过 IO MUX 与 GPIO37~GPIO38 和 SPI2 的一组八线接口管脚复用。

LP UART 接口通过 LP GPIO 交换矩阵可配置使用任意 LP GPIO 管脚。默认情况下，连接发送和接收信号（LP_UART_TXD_PAD和 LP_UART_RXD_PAD）的管脚通过 LP IO MUX 与 LP_GPIO14~LP_GPIO15 复用。

# 4.2.2.2 SPI 控制器 (SPI)

串行外设接口 (SPI) 是一种同步串行接口，可用于与外围设备进行通信。ESP32-P4 芯片集成了四个 SPI 控制器：

MSPI 控制器，简称 MSPI，包括：

– FLASH MSPI 控制器

* FLASH MSPI SPI0 

* FLASH MSPI SPI1 

– PSRAM MSPI 控制器

* PSRAM MSPI SPI0 

* PSRAM MSPI SPI1 

通用 SPI2，简称 GP-SPI2

通用 SPI3，简称 GP-SPI3

低功耗 SPI，简称 LP-SPI

# 特性

# GP-SPI 具有以下特性：

用作主机或用作从机

• 支持半双工通信和全双工通信

支持 CPU 控制的传输类型以及 DMA 控制的传输类型

支持多种数据模式：

– GP-SPI2 

* 1-bit SPI 模式

* 2-bit Dual SPI 模式

* 4-bit Quad SPI 模式

* QPI 模式

* 8-bit Octal SPI 模式（仅用于主机）

* OPI 模式（仅用于主机）

– GP-SPI3 

* 1-bit SPI 模式

* 2-bit Dual SPI 模式

* 4-bit Quad SPI 模式

* * QPI 模式

时钟频率可配置

– 用作主机时：时钟频率可达 80 MHz

– 用作从机时：时钟频率可达 60 MHz

数据长度可配置

– 在 CPU 控制的主机和从机传输中：数据长度为 $\mathord { \uparrow } \sim 6 4$ 字节

– 在 DMA 控制的主机单次传输中：数据长度为 $\uparrow { \sim } 3 2$ KB

– 在 DMA 控制的主机分段配置传输中：数据长度字节数无限制

– 在 DMA 控制的从机单次或连续传输中：数据长度字节数无限制

读写数据的比特位顺序可配置

为 CPU 控制的传输和 DMA 控制的传输分别提供独立中断

时钟极性和相位可配置

四种 SPI 时钟模式：模式 $0 \sim$ 模式 3

用作主机时，提供多条 CS 线

– GP-SPI2：CS0∼CS5 

– GP-SPI3：CS0∼CS2 

• 支持访问 SPI 接口的传感器、显示屏控制器、flash 或 RAM 芯片

LP-SPI 为 GP-SPI 的精简版，其功能为 GP-SPI 功能的子集，具有以下特性：

用作主机或用作从机

支持半双工通信和全双工通信

仅支持 CPU 控制的传输类型

仅支持 1-bit SPI 数据模式

时钟频率可配置

– 用作主机时：时钟频率可达 40 MHz

– 用作从机时：时钟频率可达 40 MHZ

数据长度可配置

– 在 CPU 控制的主机和从机传输中：数据长度为 1 64 字节

读写数据的比特位顺序可配置

为 CPU 控制的传输提供中断

时钟极性和相位可配置

四种 SPI 时钟模式：模式 $0 \sim$ 模式 3

• 用作主机时，仅提供 1 条 CS 线：CS0

用作从机时，支持唤醒功能（相较于 GP-SPI，属唯一新增功能）

# 管脚分配

FLASH MSPI 控制器使用专用数字管脚，管脚序号为 27~33。

GP-SPI2 接口的管脚有两组，一组四线接口通过 IO MUX 与 GPIO6~GPIO11 复用，另一组八线接口通过 IO MUX与 GPIO28~GPIO38、UART0 接口的管脚和 EMAC 的第一组 RMII 接口的管脚复用。对 GP-SPI2 接口速度要求不高时，也可以通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

GP-SPI3 接口通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

LP-SPI 接口通过 LP GPIO 交换矩阵可配置使用任意管脚。

# 4.2.2.3 I2C 控制器 (I2C)

ESP32-P4 在主系统有两个 I2C 控制器，在低功耗系统有一个 I2C 控制器。其中，主系统中的 I2C 控制器既可作为主机又可作为从机（下文以 I2C 指代），低功耗系统中的 I2C 控制器则只可作为主机使用，在主系统休眠时仍能工作（下文以 LP_I2C 指代）。

# 特性

ESP32-P4 I2C 控制器具有以下几个特点：

支持主机模式和从机模式

支持多主机和从机通信

支持标准模式 (100 Kbit/s)

• 支持快速模式 (400 Kbit/s)

支持 7 位以及 10 位地址寻址

从机模式下支持拉低 SCL 时钟实现连续数据传输

支持可编程数字噪声滤波功能

支持从机地址和从机内存或寄存器地址的双寻址模式

# 管脚分配

I2C 控制器通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

LP_I2C 控制器通过 LP GPIO 交换矩阵可配置使用任意 LP GPIO 管脚。

# 4.2.2.4 模拟 I2C 控制器

ESP32-P4 包含两个专用于模拟电路的 I2C 接口，可与部分模拟模块通信，完成对这些模块的参数配置。每个可配置模块中均有一个 I2C 从机，并拥有各自的地址。

# 特性

仅支持主机模式

7-bit 地址寻址

传输速率可调

• 支持睡眠模式下工作（LP CPU 可用的睡眠模式）

支持双主机工作模式

# 管脚分配

模拟 I2C 接口连接芯片内部模拟组件，无需分配 IO 管脚。

# 4.2.2.5 I3C 控制器

ESP32-P4 带有一个 I3C 主机接口 (Main Master)。

# 特性

I3C 主机接口具有以下特性：

• 符合 I3C 协议

• 兼容 I2C 模式 (FM, FM+)

• 支持 SDR 模式

支持动态地址分配

• 支持 In-Band 中断

支持 DMA 传输

# 管脚分配

I3C 控制器主机接口的 SCL 和 SDA（时钟和数据）信号通过 GPIO 交换矩阵与 GPIO32~GPIO33 复用，其余信号通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.6 I2S 控制器 (I2S)

ESP32-P4 有三个标准 I2S 接口，为多媒体应用，尤其是为数字音频应用提供了灵活的数据通信接口。

# 特性

支持主机模式和从机模式

支持全双工和半双工通信

支持 TX 模块和 RX 模块独立工作或同时工作

支持多种音频标准：

– TDM Philips 标准

– TDM MSB 对齐标准

– TDM PCM 标准

– PDM 标准

支持多种 TX/RX 模式

– TDM TX 模式，最多支持 16 通道

– TDM RX 模式，最多支持 16 通道

– PDM TX 模式

* 支持原始 PDM 数据发送

* 支持将 PCM 数据转换为 PDM 数据发送（仅适用于 I2S0），最多支持 2 通道

– PDM RX 模式

* 支持原始 PDM 数据接收

* 支持将 PDM 数据转换为 PCM 数据接收（仅适用于 I2S0），最多支持 8 通道

可配置 APLL 时钟源，支持最高频率为 240 MHz

可配置高精度采样时钟，支持多种采样频率

支持 8/16/24/32 位的数据位宽

TX 模式支持同步计数器

• 支持 ETM 功能

• 支持 GDMA（仅 GDMA-AHB）

支持 I2S 接口中断

# 管脚分配

I2S 控制器通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.7 LP I2S 控制器

ESP32-P4 内置一个 LP I2S 接口，为语音活动检测 (VAD) 模块和一些低功耗模式下的数字音频应用提供了数据接收通信接口。

# 特性

RX 模块支持主机模式和从机模式

支持多种音频标准：

– TDM Philips 标准

– TDM MSB 对齐标准

– TDM PCM 标准

– PDM 标准

支持多种 RX 模式：

– TDM RX 模式，最多支持 2 通道

– PDM RX 模式

* 支持原始 PDM 数据接收

支持将 PDM 数据转换为 PCM 数据接收，最多支持 2 通道

可配置采样时钟，支持多种采样频率

支持 16 位的数据位宽

支持 LP I2S 接口中断

# 管脚分配

LP I2S 接口通过 LP GPIO 交换矩阵可配置使用任意 LP GPIO 管脚。

# 4.2.2.8 脉冲计数控制器 (PCNT)

ESP32-P4 的脉冲计数器 (PCNT) 用于记录输入脉冲的个数。

# 特性

• 四个脉冲计数控制器（单元），各自独立工作，计数范围是 1~65535

每个单元有两个独立的通道，共用一个脉冲计数控制器

• 所有通道均有输入脉冲信号和相应的控制信号

• 滤波器独立工作，过滤每个单元输入脉冲信号和控制信号的毛刺

每个通道参数如下：

1. 选择在输入脉冲信号的上升沿或下降沿计数

2. 在控制信号为高电平或低电平时可将计数模式配置为递增、递减或停止计数

最大脉冲频率： fAPB_CLK $\frac { f _ { A P B \_ C L K } } { 2 }$ 

# 管脚分配

脉冲计数控制器通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.9 USB 2.0 高速 OTG

ESP32-P4 带有一个集成了收发器的 USB 2.0 高速 OTG 外设，下文将称为 OTG_HS。该 OTG_HS 外设符合 USB2.0 协议规范，同时兼容 OTG 1.3 协议和 OTG 2.0 协议。OTG_HS 支持 USB 2.0 传输速率为 480 Mbit/s 的高速模式 (High-Speed, HS)、传输速率为 12 Mbit/s 的全速模式 (Full-Speed, FS) 和传输速率为 1.5 Mbit/s 的低速模式 (Low-Speed, LS)。

• 处于高速模式和全速模式的 OTG_HS 可配置成 Host，也可以配置成 Device。

处于低速模式的 OTG_HS 只可配置成 Host。

# 特性

# 通用特性

• 兼容 USB 2.0 协议、OTG 1.3 协议、OTG 2.0 协议

支持高速速率、全速速率、低速速率

在全速和高速模式下既可作为主机，也可以充当设备

动态分配 FIFO (DFIFO) 大小，每个设备 EP/主机通道最大可动态分配 4 KB FIFO

• 每个微帧最大支持 8 个非周期性和 16 个周期性事务

支持多种存储器访问模

– Scatter/Gather DMA 模式

– Buffer DMA 模式

– Slave 模式

集成 UTMI 高速收发器

# 设备模式 (Device mode) 特性

端点 0 永远存在，双向控制，由 EP0 IN 和 EP0 OUT 组成

15 个附加端点 ~↑5，可配置为 IN 或 OUT

• 最多 8 个 IN 端点同时工作，包括 EP0 IN

所有 OUT 端点共享一个 RX FIFO

每个 IN 端点都有专用的 TX FIFO

# 主机模式 (Host mode) 特性

• 16 个主机通道

• 一个 RX FIFO：由所有周期事务和非周期事务共用

两个 TX FIFO：

– 所有非周期事务传输共用一个 TX FIFO

– 所有周期事务传输共用另一个 TX FIFO

上述所有 FIFO 共用 4 KB RAM

每个 FIFO 大小可配置，最大 4 KB

# 管脚分配

USB 2.0 高速 OTG 接口的 USB2 OTG PHY DM (USB_D-) 和 USB2 OTG PHY DP (USB_D+) 使用专用数字管脚，管脚序号为 49~50。其余信号通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.10 USB 2.0 全速 OTG

ESP32-P4 带有一个集成了收发器的 USB 2.0 全速 OTG 外设，下文将称为 OTG_FS。该 OTG_FS 外设可配置成主机模式 (Host mode) 或设备模式 (Device mode)，符合 USB 2.0 协议，同时兼容 OTG 1.3 协议和 OTG 2.0 协议。支持传输速率为 12 Mbit/s 的 USB 2.0 全速模式 (Full-Speed, FS) 和传输速率为 1.5 Mbit/s 的 USB 2.0 低速模式 (Low-Speed, LS)，还支持主机协商协议 (Host Negotiation Protocol, HNP) 和会话请求协议 (Session RequestProtocol, SRP)。

# 特性

# 通用特性

• 兼容 USB 2.0 协议、OTG 1.3 和 OTG 2.0 协议

支持 USB 2.0 全速和低速速率

• 主机协商协议 (HNP) 和会话请求协议 (SRP)，均可作为 A 或 B 设备

动态分配 FIFO (DFIFO) 大小，最大容量 1 KB

支持多种存储器访问模

– Scatter/Gather DMA 模式

– Buffer DMA 模式

– Slave 模式

集成 2 个内部收发器

# 设备模式 (Device mode) 特性

端点 0 永远存在，双向控制，由 EP0 IN 和 EP0 OUT 组成

6 个附加端点 1~6，可配置为 IN 或 OUT

最多 5 个 IN 端点同时工作，包括 EP0 IN

所有 OUT 端点共享一个 RX FIFO

每个 IN 端点都有专用的 TX FIFO

# 主机模式 (Host mode) 特性

8 个主机通道

• 一个 RX FIFO：由所有周期事务和非周期事务共用

两个 TX FIFO：

– 所有非周期事务传输共用一个 TX FIFO

– 所有周期事务传输共用另一个 TX FIFO

上述所有 FIFO 共用 1 KB RAM

每个 FIFO 大小可配置，最大 1 KB

# 管脚分配

两对 USB PHY 的 D+ 和 D- 端口与 GPIO24~GPIO25 和 GPIO26~GPIO27 复用。USB 2.0 全速 OTG 接口可以选择使用哪个 PHY，默认与 GPIO26~GPIO27 复用，USB_D- 和 USB_D+ 两个管脚的功能可以互换。

其余信号通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.11 USB 串口/JTAG 控制器 (USB_SERIAL_JTAG)

ESP32-P4 中包含一个 USB 串口/JTAG 控制器，可用于烧录芯片的外部 flash、读取程序输出的数据以及将调试器连接到正在运行的程序中。

# 特性

兼容 USB 2.0 全速标准，传输速度最高可达 12 Mbit/s（注意，该控制器不支持 480 Mbit/s 的高速传输模式） 

包含 CDC-ACM 虚拟串口及 JTAG 适配器功能

烧录芯片 flash

• 利用紧凑的 JTAG 指令，支持 CPU 调试

芯片内部集成的全速 USB PHY

集成两个全速收发器

可选择连接至 GPIO24/GPIO25 或者 GPIO26/GPIO27 其中任意一个全速集成收发器

与 USB 2.0 全速 OTG 控制器同时使用时，USB 2.0 全速 OTG 控制器与 USB 串口/JTAG 控制器需要使用不同的集成收发器

# 管脚分配

两对 USB PHY 的 D+ 和 D- 端口与 GPIO24~GPIO25 和 GPIO26~GPIO27 复用。USB 串口/JTAG 控制器接口可以选择使用哪个 PHY，默认与 GPIO24~GPIO25 复用。

# 4.2.2.12 以太网介质访问控制器 (EMAC)

借助外部以太网物理层 (Ethernet PHY)，ESP32-P4 可以通过以太网介质访问控制 (Ethernet MAC) 按照 IEEE802.3 标准发送和接收数据。

ESP32-P4 以太网 MAC 符合以下标准：

• 符合 IEEE 802.3-2002，用于以太网 MAC。

符合 IEEE 1588-2008 标准，用于规定联网时钟同步的精度。

• 符合 IEEE 802.3 规范工业标准接口：介质独立接口 (MII) 和简化介质独立接口 (RMII)。

符合 IEEE 802.3az － 2010 节能以太网标准

• 符合 IEEE 802.1Q 标准，用于支持 VLAN 帧

# 特性

支持外部 PHY 接口实现 10/100 Mbit/s 数据传输速率

• 可通过符合 IEEE802.3 的 MII 接口或 RMII 接口与外部快速以太网 PHY 进行通信（一次仅可使用一种接口）

支持全双工和半双工模式

– 支持适用于半双工模式的 CSMA/CD 协议

– 支持适用于全双工模式的 IEEE 802.3x 流量控制

– 全双工模式时可以将接收的暂停控制帧转发到用户应用程序

– 半双工模式时提供背压流量控制

– 全双工操作中如果流量控制输入信号消失，将自动发送暂停时间为零的暂停帧

报头和帧起始数据 (SFD) 在发送路径中插入、在接收路径中删除

• 可逐帧控制 CRC 和 padding（全 0）自动生成

• 如果数据为达到最小帧长度，则自动添加 padding

可编程帧长度，支持高达 16 KB 的巨型帧

• 可编程帧间隔 (IFG)（40-96 位时间，以 8 为步长）

支持多种灵活的地址过滤模式:

– 高达 8 个 48 位完美地址过滤器，对每个字节进行掩码操作

– 高达 8 个 48 位 SA 地址比较检查，对每个字节进行掩码操作

– 可传送所有多播地址帧

– 支持混合模式，因此可传送所有帧，无需为网络监视进行过滤

– 传送所有传入数据包时（每次过滤时）均附有一份状态报告

为发送和接收数据包分别返回 32 位状态

在接收功能中支持 VLAN 标记帧过滤

• 为应用程序提供单独的发送、接收和控制接口

使用 MDIO 接口配置和管理 PHY 设备

在接收功能中支持对接收到的由以太网帧封装的 IPv4 和 TCP 数据包进行校验和卸载

在接收功能中支持检查 IPv4 头校验和以及在 IPv4/IPv6 数据包中封装的 TCP、UDP 或 ICMP 校验和

• 支持以太网帧时间戳（详细参考 IEEE 1588-2008）。每个帧在发送或接收时带有 64 位时间戳。

• 支持节能以太网（详细参考 IEEE 802.3az-2010）

支持传输帧中 CRC 替换、源地址字段插入或替换以及 VLAN 插入、替换或删除

• 两组 FIFO：一个 256 字节发送 FIFO 和一个 256 字节接收 FIFO

接收 FIFO 进行多帧存储时，在 EOF 传输后，通过向接收 FIFO 插入接收状态矢量，从而使得接收 FIFO 无需存储这些帧的接收状态

• 可以转发过小的好帧

• 为接收 FIFO 中由于溢出丢失或损坏的帧生成脉冲，借此支持数据统计

发送时处理冲突帧的自动重新发送

丢弃延迟冲突、过度冲突、过度延迟和下溢条件下的帧

通过软件控制刷新 TX FIFO

# 管脚分配

以太网介质访问控制器 (EMAC) 仅包含一个 RMII 接口，但该接口的每根信号线均提供三组管脚位置可选，可通过 IO MUX 独立配置到以下任意一组管脚：

第一组管脚与 GPIO28~GPIO36 和 SPI2 的一组八线接口管脚复用。

• 第二组管脚与 GPIO40~GPIO48 复用。

第三组管脚与 GPIO49~GPIO54 复用，其中仅包含发送使能信号 (RMII_TXEN)，不包含其他发送信号。用户可为 RMII 接口中的每根信号单独选择上述三组管脚中的任意一组进行引脚分配。MII 接口、MDIO 接口以及其他接口通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.13 双线汽车接口 (TWAI)

ESP32-P4 包含三个 TWAI 控制器，任意控制器都可通过外部收发器连接到 TWAI 总线。

# 特性

• 兼容 ISO 11898-1 协议（CAN 规范 2.0）

支持标准格式（11 位标识符）和扩展格式（29 位标识符）两种帧格式

支持 1 Kbit/s ~ 1 Mbit/s 位速率

支持多种操作模式：

– 正常模式

– 只听模式（不影响总线）

– 自测模式（发送数据时无需应答）

配置 64 字节接收 FIFO

支持特殊发送：

– 单次发送（发生错误时不会自动重新发送）

– 自发自收（TWAI 控制器同时发送和接收报文）

• 配置数据接收过滤器（支持单过滤器和双过滤器模式）

• 支持错误检测与处理

– 配置错误计数器

– 可配置错误报警阈值

– 内置错误代码记录

– 内置仲裁丢失记录

支持收发器自动待机功能

# 管脚分配

双线汽车接口通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.14 SD/MMC 主机控制器 (SDHOST)

ESP32-P4 集成一个 SD/MMC 主机控制器。

# 特性

支持两个外部卡

支持 3.0、3.01 版本 SD 存储卡标准

支持 3.0 版本 SDIO

支持 4.41、4.5、4.51 版本 MMC

支持 1.1 版本 CE-ATA

支持 1-bit、4-bit 和 8-bit 位宽模式

# 管脚分配

SD/MMC 主机控制器的卡 1 (SDMMC_HOST_SLOT_0) 信号通过 IO MUX 与 GPIO39~GPIO48 和 EMAC RMII 第二组接口及 50 MHz 时钟输出管脚复用。卡 2 (SDMMC_HOST_SLOT_1) 信号通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.15 LED PWM 控制器 (LEDC)

LED PWM 控制器用于生成控制 LED 的脉冲宽度调制信号 (PWM)，具有占空比自动渐变等功能。该外设也可生成 PWM 信号用作其他用途。

# 特性

• 八个独立的 PWM 生成器（即八个通道）

• PWM 占空比最大精度为 20 位

四个独立定时器，可实现小数分频

PWM 输出信号相位可调节

• PWM 占空比微调

占空比自动渐变—即 PWM 信号占空比可逐渐增加或减小，无须处理器干预，渐变完成时产生中断

每个PWM生成器包含16个占空比渐变区间，用于生成占空比伽马曲线渐变的信号。每个区间都可以独立配置占空比变化方向（增加或减少）、变化步长、变化次数以及变化频率

• 低功耗模式 (Light-sleep mode) 下可输出 PWM 信号

可以生成 ETM（事件任务矩阵）外设相关的事件，可以接收 ETM 外设相关的任务

# 管脚分配

LED PWM 控制器通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.16 电机控制脉宽调制器 (MCPWM)

ESP32-P4包含两个电机控制脉宽调制器(MCPWM)，可以用于驱动数字马达和智能灯。每个MCPWM外设包含一个时钟分频器（预分频器）、三个 PWM 定时器、三个 PWM 操作器、一个捕获模块、一个 ETM 模块和一个故障检测模块。

# 特性

PWM 定时器用于生成定时参考。PWM 操作器将根据定时参考生成所需的波形。通过配置，任一 PWM 操作器可以使用任一 PWM 定时器的定时参考。不同的 PWM 操作器可以使用相同的 PWM 定时器的定时参考来产生PWM 信号。此外，不同的 PWM 操作器也可以使用不同的 PWM 定时器的值来生成单独的 PWM 信号。不同的PWM 定时器也可进行同步。

# 管脚分配

电机控制脉宽调制器通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.17 红外遥控 (RMT)

红外遥控器 (RMT) 支持四通道的红外发射和四通道的红外接收。通过程序控制脉冲波形，遥控器可以支持多种红外协议和单线协议。

# 特性

共配置八个通道：

– 0~3 通道支持发送

– 4~7 通道支持接收

– 八个通道共享 $3 8 4 \times 3 2$ 位的 RAM

发射器支持以下模式：

– 普通发送模式

– 乒乓发送模式

– 持续发送模式

– 载波调制

– 多通道同时发送

– 发送通道 3 支持 GDMA 访问

接收器支持以下模式：

– 普通接收模式

– 乒乓接收模式

– 接收滤波

– 载波解调

– 接收通道 7 支持 GDMA 访问

# 管脚分配

红外遥控通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.18 并行 IO 控制器 (PARLIO)

ESP32-P4 包含一个并行 IO 控制器 (PARLIO)，支持通过通用直接存储访问 (GDMA) 在并行总线上实现外部设备和内部存储器之间的数据通信。

# 特性

• 支持多种时钟源可选：

– 包括外部 IO 时钟 PAD_CLK_TX/RX、内部系统时钟 XTAL_CLK、PLL_F160M_CLK 和 RC_FAST_CLK

– 最大支持 40 MHz 的 IO 时钟频率

– 时钟支持整数和小数分频

支持将传输数据总线位宽配置为 1/2/4/8/16 位

支持 16 位全双工传输

总线位宽为 1/2/4 位时，支持在一个字节范围内对比特数据顺序进行翻转

包含用于接收 IO 并行数据的 RX 子模块：

– 支持对输出时钟进行门控

– 支持 RX 子模块输入时钟和输出时钟分别取反

– 支持多种接收模式

– 支持配置 GDMA SUC EOF 信号生成模式

– 支持配置外部使能信号的 IO 管脚

包含用于发送 IO 并行数据的 TX 子模块：

– 支持对输出时钟进行门控

– 支持 TX 子模块输入时钟和输出时钟分别取反

– 支持有效信号输出

– 支持配置 TX EOF 信号生成模式

– 支持配置总线空闲时数值

# 管脚分配

并行 IO 控制器通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

# 4.2.2.19 比特调节器

ESP32-P4 中有大量支持 DMA（直接存储器访问）的外设，它们可以在 CPU 不参与的情况下将数据从存储器传输到外设或从外设传输到存储器，但这需要外设传输的数据格式与软件支持的数据格式相同，如果格式不同，则需要 CPU 重写数据格式，如交换字节、反转字节和左右移位数据。

由于位操作通常相当耗费 CPU 资源，而设计 DMA 的初衷是在传输过程中避免使用 CPU，因此 ESP32-P4 集成了两个比特调节器 (BitScrambler)，专门用于修改存储器和外设之间传输数据的格式，一个传输控制器用于存储器到外设（或存储器到存储器）方向的传输，另一个传输控制器用于外设到存储器方向的传输。除此之外，比特调节器还是一个灵活的可编程状态机，能够执行更高级的操作。

# 特性

• 两个比特调节器，一个用于 RX（外设到存储器），一个用于 TX（存储器到外设）

支持存储器到存储器的传输

每个 DMA 时钟周期最多可处理 32 位数据

数据路径由存储在指令存储器中的比特调节器程序控制

• 输入寄存器每个时钟周期可读取 0、8、16 或 32 位

输出寄存器：

– 每个时钟周期可写入 0、8、16 或 32 位

– 输出寄存器位的数据源：64 位输入数据、两个计数器、LUT RAM 数据、上个周期的数据输出、比较器

– 32 位输出寄存器位中的每一位可以来自数据源的任意位

8 x 257 位指令存储器，用于存储八条指令，配置控制流和数据路径

2048 字节查找表 (LUT) 存储器，可配置为不同的字宽

# 管脚分配

比特调节器无需直接与 IO 进行交互，因此无需分配管脚。

# 4.2.3 模拟信号处理

本小节描述芯片上感知和处理现实世界数据的组件。

# 4.2.3.1 触摸传感器

ESP32-P4 提供了多达 14 个电容式传感 GPIO，能够探测由手指或其他物品直接接触或接近而产生的电容差异。这种设计具有低噪声和高灵敏度的特点，可以用于支持使用相对较小的触摸板。设计中也可以使用触摸板阵列以探测更大区域或更多点。ESP32-P4 的触摸传感器同时还支持防水、跳频检测和数字滤波等功能来进一步提高传感器的性能。

# 特性

支持 14 个电容触摸管脚的检测

可由软件或专用硬件定时器触发采样操作

支持两种采样方式：

– 将来自触摸管脚的脉冲序列信号作为时钟信号处理，利用该时钟来计数采样周期

– 将来自触摸管脚的脉冲序列信号作为数字信号处理，利用系统时钟采样该数字信号的上升沿来计数采样周期

支持扫描模式，可配置 Touch FSM 按照固定顺序对多个触摸管脚进行采样

支持超时机制，监测通道异常

支持跳频采样，增加检测的抗干扰性

支持接近感应模式，最多可配置三个通道

支持配置单个触摸传感器在休眠模式时正常工作

支持触摸传感器用作唤醒源

支持防潮功能

支持遇水保护功能

# 管脚分配

触摸传感器接口与 GPIO2~GPIO15、LP_GPIO2~LP_GPIO15、LP_UART 接口和 SPI2 的一组四线接口管脚复用。配置模拟功能生效时，与其复用的数字功能无效。

# 4.2.3.2 温度传感器 (TSENS)

ESP32-P4 配备了一个温度传感器，用于实时测量芯片内部温度。温度传感器能将输出电压转换成数字值，并具有补偿温度偏移的功能。

# 特性

• 支持软件触发测量温度，且一旦触发后，传感器可持续测量温度，软件可实时读取数据

支持硬件触发自动监测温度，支持两种自动监测唤醒模式

• 支持根据使用环境配置温度偏移，提高测试精度

温度测量范围可配置

支持多个事件任务矩阵 (ETM) 相关的事件和任务

# 管脚分配

温度传感器无需直接与 IO 进行交互，因此无需分配管脚。

# 4.2.3.3 ADC 控制器 (ADC)

ESP32-P4 内置了两个 12 位的逐次逼近型模拟数字转换器 (SAR ADC)，可测量最多来自 14 个管脚的模拟信号。

# 特性

支持 HP ADC 控制器和 LP ADC 控制器通过软件选择的方式获取 SAR ADC 的控制权

支持 12 位采样分辨率

支持采集最多 14 个管脚上的模拟信号

HP ADC 控制器：

– 配有多通道采样控制模块，支持多通道采样模式，采样通道顺序可配

– 提供模式控制模块，支持双 HP ADC 采样

– 提供两个滤波器，滤波系数可配

– 提供两个阈值监控器，滤波数据大于设置的高阈值或小于设置的低阈值将产生中断

– GDMA 连续数据搬运

LP ADC 控制器：

– 支持单次采样模式

– 支持在低功耗模式（如 Deep-sleep）下工作

• 支持多个事件任务矩阵 (ETM) 相关的事件和任务

# 管脚分配

模/数转换器接口与 GPIO16~GPIO23、GPIO49~GPIO54 和模拟电压比较器接口、EMAC 的第三组 RMII 接口管脚复用。

# 4.2.3.4 模拟电压比较器

ESP32-P4 芯片集成了两个模拟电压比较器。模拟电压比较器依靠支持电压比较功能的特殊芯片焊盘 (PAD) 实现，用于监测 PAD 上的电压变化。

# 特性

支持电压比较功能

– 电压比较模式可配置

– 内部参考电压值可配置

支持电压比较中断

支持 ETM 事件

# 管脚分配

模拟电压比较器接口与 GPIO51~GPIO52、GPIO53~GPIO54 和模/数转换器接口、EMAC 的第三组 RMII 接口管脚复用。

# 4.2.3.5 语音活动检测 (VAD)

ESP32-P4 集成了语音活动检测 (VAD) 模块，硬件实现了语音唤醒等多媒体功能的第一阶段算法。此外，它还为低功耗语音唤醒解决方案提供硬件支持。

# 特性

• VAD 算法按帧处理音频数据，每帧 256 个数据点，数据采样率为 8 kHz，位宽 16 位

2 KB 缓存，可保留多达 4 帧数据

独立的系统唤醒源

可配置中断源

算法参数可灵活配置

# 管脚分配

VAD 模块无需直接与 IO 进行交互，因此无需分配管脚。

# 5 电气特性

说明：

本章节提供的电气特性数据暂供参考，在规格书终版发布时可能会更新。

# 5.1 绝对最大额定值

超出表 5-1 绝对最大额定值 的绝对最大额定值可能导致器件永久性损坏。这只是强调的额定值，不涉及器件在这些或其它条件下超出章节 5.2 建议工作条件 技术规格指标的功能性操作。长时间暴露在绝对最大额定条件下可能会影响设备的可靠性。


表 5-1. 绝对最大额定值


| 参数 | 说明 | 最小值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- |
| VDD_LDO, VDD_DCDCC, VDD_ANA, VDD_BAT, VDD_LP | 允许输入电压 | -0.3 | 3.6 | V |
| VDD_IO_0, VDD_FLASHIO³, VDD_IO_4, VDD_IO_5, VDD_IO_6 | 允许输入电压 | 1.62/-0.3 | 1.98/3.6 | V |
| VDD_PSRAM_0, VDD_PSRAM_1 | 允许输入电压 | 1.62 | 1.98 | V |
| VDD_HP_0, VDD_HP_1, VDD_HP_2, VDD_HP_3 | 允许输入电压 | 0 | 1.3 | V |
| VDD_MIPI_DPHY | 允许输入电压 | 0 | 2.75 | V |
| VDD_USBPHY | 允许输入电压 | -0.66 | 3.96 | V |
| I_output² | IO 输出总电流 | - | 1500 | mA |
| TSTORE | 存储温度 | -40 | 150 | °C |


1 更多关于输入电源管脚的信息，见章节 2.6.1 电源管脚。



2 在 $2 5 ^ { \circ } \mathrm { C }$ 的环境温度下连续 24 小时保持所有 IO 管脚拉高并接地，设备工作完全正常。



3 VDD_FLASHIO 给 flash IO 供电，因此具体电压需要根据 flash 型号确定。


# 5.2 建议工作条件


表 5-2. 建议工作条件


| 参数 | 说明 | 最小值 | 典型值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- | --- |
| VDD_LDO, VDD_DCDCC, VDD_ANA, VDD_LP | 建议输入电压 | 3.0 | 3.3 | 3.6 | V |
| VDD_BAT | 建议输入电压 | 2.5 | 3.3 | 3.6 | V |
| VDD_IO_0, VDD_FLASHIO, VDD_IO_4, VDD_IO_5, VDD_IO_6 | 建议输入电压 | 1.65/3.0 | 1.8/3.3 | 1.95/3.6 | V |
| VDD_PSRAM_0, VDD_PSRAM_1 | 建议输入电压 | 1.65 | 1.8 | 1.95 | V |
| VDD_HP_0, VDD_HP_1, VDD_HP_2, VDD_HP_31 | 建议输入电压 | 0.99 | 1.1 | 1.3 | V |

见下页


表 5-2 – 接上页


| 参数 | 说明 | 最小值 | 典型值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- | --- |
| VDD_MIPI_DPHY | 建议输入电压 | 2.25 | 2.5 | 2.75 | V |
| VDD_USBPHY | 建议输入电压 | 2.97 | 3.3 | 3.63 | V |
| I VDD | Core的供电电流 | 0.5 | - | - | A |
| TA | 环境温度 | -40 | - | 85 | °C |


1 芯片可以根据情况自动调节 VDD_HP_x 的输入电压


# 5.3 VDDO_FLASH 输出特性


表 5-3. VDDO_FLASH 内部和输出特性


| 参数 | 说明 | 典型值 | 单位 |
| --- | --- | --- | --- |
| RVFB | VDDO_FLASH 连接 3.3 V flash 时,由 VDD_LDO 经 RVFB 供电1 | 3 | Ω |
| lVFB | VDDO_FLASH 连接 1.8 V flash 时,Flash LDO 的输出电流 | 50 | mA |


1 请结合章节 2.6.2 电源管理 阅读。



1 VDD_LDO 需高于 VDD_flash_min + I_flash_max × RV F B，


其中

VDD_flash_min – flash 的最小工作电压

I_flash_max – flash 的最大工作电流

# 5.4 直流电气特性 (3.3 V, 25 °C)


表 5-4. 直流电气特性 (3.3 V, 25 °C)


| 参数 | 说明 | 最小值 | 典型值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- | --- |
| CIN | 管脚电容 | - | 2 | - | pF |
| VIH | 高电平输入电压 | 0.75 × VDD1 | - | VDD1 + 0.3 | V |
| VIL | 低电平输入电压 | -0.3 | - | 0.25 × VDD1 | V |
| IH | 高电平输入电流 | - | - | 50 | nA |
| IL | 低电平输入电流 | - | - | 50 | nA |
| VOH2 | 高电平输出电压 | 0.8 × VDD1 | - | - | V |
| VOL2 | 低电平输出电压 | - | - | 0.1 × VDD1 | V |
| IOH | 高电平拉电流 (VDD1 = 3.3 V, VOH &gt;= 2.64 V, PAD Driver = 3) | - | 40 | - | mA |
| IOL | 低电平灌电流 (VDD1 = 3.3 V, VOL = 0.495 V, PAD Driver = 3) | - | 28 | - | mA |
| RPU | 内部弱上拉电阻 | - | 45 | - | kΩ |
| RPD | 内部弱下拉电阻 | - | 45 | - | kΩ |
| VIH_nRST | 芯片复位释放电压（CHIP_PU应满足电压范围） | 0.75 × VDD_BAT | - | VDD_BAT + 0.3 | V |
| VIL_nRST | 芯片复位电压（CHIP_PU应满足电压范围） | -0.3 | - | 0.25 × VDD_BAT | V |

1 VDD 是电源管脚 VDD_IO_0/4/5/6 的电压。

V_OH 和 V_OL 为负载是高阻条件下的测试值。

# 5.5 ADC 特性

本章节数据是在 ADC 外接 100 nF 电容、输入为 DC 信号、 25°C 环境温度的测量结果。


表 5-5. ADC 特性


| 符号 | 最小值 | 最大值 | 单位 |
| --- | --- | --- | --- |
| DNL（差分非线性）1 | -1 | 3 | LSB |
| INL（积分非线性） | -5 | 3 | LSB |
| 采样速度 | — | 100 | kSPS2 |

1 使用滤波器多次采样或计算平均值可以获得更好的 DNL 结果。

2 kSPS (kilo samples-per-second) 表示每秒采样千次。

ADC经硬件校准和软件校准后的结果如表5-6ADC特性所示。如需更高的精度，可选用其他方法自行校准。


表 5-6. ADC 校准结果


| 参数 | 说明 | 最小值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- |
| 总误差 | ATTENO,有效测量范围0~1000 | -12 | 12 | mV |
| ATTEN1,有效测量范围0~1300 | -12 | 12 | mV |
| ATTEN2,有效测量范围0~1900 | -12 | 12 | mV |
| ATTEN3,有效测量范围0~3300 | -15 | 15 | mV |

# 5.6 Active 模式与低功耗模式下的功耗

下列各模式功耗数据是基于 3.3 V 供电电源、 25°C 环境温度的条件下测得。


表 5-7. Active 模式下的功耗


| 工作模式 | 频率 (MHz) | 说明 | 典型值¹ (mA) | 典型值² (mA) |
| --- | --- | --- | --- | --- |
|  | 400 | WAITI（双核均空闲） | 23 | 56 |
| 双核均运行 while(1) | 69 | 112 |
| 单核运行 CoreMark，另一个核空闲 | 66 | 110 |
| 双核执行 32 位数据访问指令 | 97 | 150 |
| 200 | WAITI（双核均空闲） | 21 | 54 |
| 双核均运行 while(1) | 44 | 87 |

见下页


表 5-7 – 接上页


| 工作模式 | 频率(MHz) | 说明 | 典型值¹(mA) | 典型值²(mA) |
| --- | --- | --- | --- | --- |
|  |  | 单核运行 CoreMark, 另一个核空闲 | 43 | 86 |
| 双核执行 32 位数据访问指令 | 58 | 100 |


见下页



表 5-7 – 接上页


| 工作模式 | 频率 (MHz) | 说明 | 典型值¹ (mA) | 典型值² (mA) |
| --- | --- | --- | --- | --- |
|  | 100 | WAITI（双核均空闲） | 17 | 40 |
| 双核均运行 while(1) | 29 | 56 |
| 单核运行 CoreMark，另一个核空闲 | 29 | 55 |
| 双核执行 32 位数据访问指令 | 36 | 63 |
| 40 | WAITI（双核均空闲） | 15 | 30 |
| 双核均运行 while(1) | 19 | 37 |
| 单核运行 CoreMark，另一个核空闲 | 19 | 37 |
| 双核执行 32 位数据访问指令 | 22 | 39 |


1 所有外设时钟关闭时的典型值。



2 所有外设时钟打开时的典型值。实际情况下，外设在不同工作状态下电流会有所差异。



3 Active 模式下，访问 flash/PSRAM 时功耗会增加。



表 5-8. 低功耗模式下的功耗


| 工作模式 | 说明 | 典型值 (mA)1 |
| --- | --- | --- |
| Light-sleep2 | 所有 GPIO 设置为高阻状态，所有电源都不断电 | 0.8 |
| 所有 GPIO 设置为高阻状态，大部分外设断电，USB 保持连接 | 0.085 |
| 所有外设断电，HP memory 保持数据 | 0.075 |
| Deep-sleep | LP 定时器和 LP 存储器上电 | 0.012 |
| 关闭 | CHIP_PU 管脚拉低，芯片关闭 | 0.001 |


1 功耗数据是在 USB 2.0 未工作状态下测得。



2 Light-sleep 状态下的电流是指 PSRAM 未供电时的测量得到的电流。Light-sleep 状态下，如果 PSRAM 处于工作状态，芯片内部的电流将额外增加约 0.1 mA，同时还会叠加 PSRAM对应模式的电流。


# 5.7 存储器规格

本节数据来源于存储器供应商的数据手册。以下数值已在设计阶段和/或特性验证中得到确认，但未在生产中进行全面测试。设备出厂时，存储器均为擦除状态。


表 5-9. Flash 规格


| 参数 | 说明 | 最小值 | 典型值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- | --- |
| VCC | 电源电压(1.8V) | 1.65 | 1.80 | 2.00 | V |
| 电源电压(3.3V) | 2.7 | 3.3 | 3.6 | V |
| FC | 最大时钟频率 | 80 | - | - | MHz |
| - | 编程/擦除周期 | 100,000 | - | - | 次 |
| TRET | 数据保留时间 | 20 | - | - | 年 |
| TPP | 页编程时间 | - | 0.8 | 5 | ms |
| TSE | 扇区擦除时间(4KB) | - | 70 | 500 | ms |

见下页


表 5-9 – 接上页


| 参数 | 说明 | 最小值 | 典型值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- | --- |
| TBE1 | 块擦除时间(32 KB) | - | 0.2 | 2 | s |
| TBE2 | 块擦除时间(64 KB) | - | 0.3 | 3 | s |
| TCE | 芯片擦除时间(16 Mb) | - | 7 | 20 | s |
| 芯片擦除时间(32 Mb) | - | 20 | 60 | s |
| 芯片擦除时间(64 Mb) | - | 25 | 100 | s |
| 芯片擦除时间(128 Mb) | - | 60 | 200 | s |
| 芯片擦除时间(256 Mb) | - | 70 | 300 | s |


表 5-10. PSRAM 规格


| 参数 | 说明 | 最小值 | 典型值 | 最大值 | 单位 |
| --- | --- | --- | --- | --- | --- |
| VCC | 电源电压(1.8V) | 1.62 | 1.80 | 1.98 | V |
| 电源电压(3.3V) | 2.7 | 3.3 | 3.6 | V |
| FC | 最大时钟频率 | 80 | - | - | MHz |

# 6 封装

有关卷带、载盘和产品标签的信息，请参阅 《ESP32-P4 芯片包装信息》。

俯视图中，芯片管脚从 Pin 1 位置开始按逆时针方向编号。关于管脚序号和名称的详细信息，请参考图 2-1ESP32-P4 管脚布局（俯视图）。




|  | SYMBOL | MIN | NOM | MAX |
| --- | --- | --- | --- | --- |
| TOTAL THICKNESS | A | 0.8 | 0.85 | 0.9 |
| STAND OFF | A1 | 0 | 0.02 | 0.05 |
| MOLD THICKNESS | A2 | ---- | 0.65 | ---- |
| L/F THICKNESS | A3 | 0.203 REF |
| LEAD WIDTH | b | 0.13 | 0.18 | 0.23 |
| BODY SIZE | X | D | 10 BSC |
| Y | E | 10 BSC |
| LEAD PITCH | e | 0.35 BSC |
| EP SIZE | X | D2 | 7.4 | 7.5 | 7.6 |
| Y | E2 | 7.4 | 7.5 | 7.6 |
| LEAD LENGTH | L | 0.3 | 0.4 | 0.5 |
| L1 | 0.35 REF |
| LEAD TIP TO EXPOSED PAD EDGE | K | 0.85 REF |
| PACKAGE EDGE TOLERANCE | aaa | 0.1 |
| MOLD FLATNESS | ccc | 0.1 |
| COPLANARITY | eee | 0.08 |
| LEAD OFFSET | bbb | 0.07 |
| EXPOSED PAD OFFSET | fff | 0.1 |


NOTES 1.REFER TOJEDEC MO-220: 2.COPLANARITY APPLIES TO LEADS，CORNER LEADS AND DIE ATTACH PAD: 3.CANANUSFTHFPIES1ENVR,NMFNT−EEATEASUBSTANCES 4.FINISH:Cu/EP·Sn8~20s 



图 6-1. QFN104 (10×10 mm) 封装


# 相关文档和资源

# 相关文档

《ESP32-P4 技术参考手册》 – 提供 ESP32-P4 芯片的存储器和外设的详细使用说明。

《ESP32-P4 硬件设计指南》 – 提供基于 ESP32-P4 芯片的产品设计规范。

《ESP32-P4 系列芯片勘误表》 – 描述 ESP32-P4 系列芯片的已知错误。

• 证书

https://espressif.com/zh-hans/support/documents/certificates 

• ESP32-P4 产品/工艺变更通知 (PCN)

https://espressif.com/zh-hans/support/documents/pcns?keys=ESP32-P4 

• ESP32-P4 公告 – 提供有关安全、bug、兼容性、器件可靠性的信息

https://espressif.com/zh-hans/support/documents/advisories?keys=ESP32-P4 

文档更新和订阅通知

https://espressif.com/zh-hans/support/download/documents 

# 开发者社区

《ESP32-P4 ESP-IDF 编程指南》 – ESP-IDF 开发框架的文档中心。

• ESP-IDF 及 GitHub 上的其它开发框架

https://github.com/espressif 

ESP32 论坛 – 工程师对工程师 (E2E) 的社区，您可以在这里提出问题、解决问题、分享知识、探索观点。

https://esp32.com/ 

ESP-FAQ – 由乐鑫官方推出的针对常见问题的总结。

https://espressif.com/projects/esp-faq/zh_CN/latest/index.html 

The ESP Journal – 分享乐鑫工程师的最佳实践、技术文章和工作随笔。

https://blog.espressif.com/ 

SDK 和演示、App、工具、AT 等下载资源

https://espressif.com/zh-hans/support/download/sdks-demos 

# 产品

ESP32-P4 系列芯片 – ESP32-P4 全系列芯片。

https://espressif.com/zh-hans/products/socs?id=ESP32-P4 

• ESP32-P4 系列开发板 – ESP32-P4 全系列开发板。

https://espressif.com/zh-hans/products/devkits?id=ESP32-P4 

• ESP Product Selector（乐鑫产品选型工具）– 通过筛选性能参数、进行产品对比快速定位您所需要的产品。

https://products.espressif.com/#/product-selector?language=zh 

# 联系我们

商务问题、技术支持、电路原理图 & PCB 设计审阅、购买样品（线上商店）、成为供应商、意见与建议

https://espressif.com/zh-hans/contact-us/sales-questions 

# 附录 A – ESP32-P4 管脚总览

ESP32-P4 管脚总览 Excel 文件可供下载。

| 管脚序号 | 管脚名称 | 管脚类型 | 供电管脚 | 管脚配置 | IO MUX功能 | LP IO MUX功能 | 模拟功能 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 复位时 | 复位后 | FO | 类型 | F1 | 类型 | F2 | 类型 | F3 | 类型 | FO | 类型 | F1 | 类型 | F0 | F1 |
| 1 | GPIO1 | IO | VDD_LP/VDD_BAT | - | - | GPIO1 | I/O/T | GPIO1 | I/O/T | - | - | - | - | LP_GPIO1 | I/O/T | LP_G PIO1 | I/O/T | XTAL_32K_P | - |
| 2 | GPIO2 | IO | VDD_LP/VDD_BAT | - | IE, WPU | MTCK | II | GPIO2 | I/O/T | - | - | - | - | LP_G PIO2 | I/O/T | LP_G PIO2 | I/O/T | TOUCH_CHANNEL1 | - |
| 3 | GPIO3 | IO | VDD_LP/VDD_BAT | - | IE | MTDI | II | GPIO3 | I/O/T | - | - | - | - | LP_G PIO3 | I/O/T | LP_G PIO3 | I/O/T | TOUCH_CHANNEL2 | - |
| 4 | GPIO4 | IO | VDD_LP | - | IE | MTMS | IO | GPIO4 | I/O/T | - | - | - | - | LP_G PIO4 | I/O/T | LP_G PIO4 | I/O/T | TOUCH_CHANNEL3 | - |
| 5 | GPIO5 | IO | VDD_LP | - | - | MTDO | O/T | GPIO5 | I/O/T | - | - | - | - | LP_G PIO5 | I/O/T | LP_G PIO5 | I/O/T | TOUCH_CHANNEL4 | - |
| 6 | GPIO6 | IO | VDD_LP | - | - | GPIO6 | I/O/T | GPIO6 | I/O/T | - | - | SPI2_HOLDPAD | I/O/T | LP_G PIO6 | I/O/T | LP_G PIO6 | I/O/T | TOUCH_CHANNEL5 | - |
| 7 | GPIO7 | IO | VDD_LP | - | - | GPIO7 | I/O/T | GPIO7 | I/O/T | - | - | SPI2_CSPAD | I/O/T | LP_G PIO7 | I/O/T | LP_G PIO7 | I/O/T | TOUCH_CHANNEL6 | - |
| 8 | GPIO8 | IO | VDD_LP | - | - | GPIO8 | I/O/T | GPIO8 | I/O/T | - | - | SPI2_DPAD | I/O/T | LP_G PIO8 | I/O/T | LP_G PIO8 | I/O/T | TOUCH_CHANNEL7 | - |
| 9 | VDD_LP | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 10 | GPIO9 | IO | VDD_LP | - | - | GPIO9 | I/O/T | GPIO9 | I/O/T | - | - | SPI2_CKPAD | I/O/T | LP_G PIO9 | I/O/T | LP_G PIO9 | I/O/T | TOUCH_CHANNEL8 | - |
| 11 | GPIO10 | IO | VDD_LP | - | - | GPIO10 | I/O/T | GPIO10 | I/O/T | - | - | SPI2_QPAD | I/O/T | LP_G PIO10 | I/O/T | LP_G PIO10 | I/O/T | TOUCH_CHANNEL9 | - |
| 12 | GPIO11 | IO | VDD_LP | - | - | GPIO11 | I/O/T | GPIO11 | I/O/T | - | - | SPI2_WPPAD | I/O/T | LP_G PIO11 | I/O/T | LP_G PIO11 | I/O/T | TOUCH_CHANNEL10 | - |
| 13 | GPIO12 | IO | VDD_LP | - | - | GPIO12 | I/O/T | GPIO12 | I/O/T | - | - | - | - | LP_G PIO12 | I/O/T | LP_G PIO12 | I/O/T | TOUCH_CHANNEL11 | - |
| 14 | GPIO13 | IO | VDD_LP | - | - | GPIO13 | I/O/T | GPIO13 | I/O/T | - | - | - | - | LP_G PIO13 | I/O/T | LP_G PIO13 | I/O/T | TOUCH_CHANNEL12 | - |
| 15 | GPIO14 | IO | VDD_LP | - | - | GPIO14 | I/O/T | GPIO14 | I/O/T | - | - | - | - | LP_UART_TXD PAD | O | LP_G PIO14 | I/O/T | TOUCH_CHANNEL13 | - |
| 16 | GPIO15 | IO | VDD_LP | - | - | GPIO15 | I/O/T | GPIO15 | I/O/T | - | - | - | - | LP_UART_RXD PAD | I1 | LP_G PIO15 | I/O/T | TOUCH_CHANNEL14 | - |
| 17 | GPIO16 | IO | VDD_IO_0 | - | - | GPIO16 | I/O/T | GPIO16 | I/O/T | - | - | - | - | - | - | - | - | ADC1_CHANNEL0 | - |
| 18 | GPIO17 | IO | VDD_IO_0 | - | - | GPIO17 | I/O/T | GPIO17 | I/O/T | - | - | - | - | - | - | - | - | ADC1_CHANNEL1 | - |
| 19 | GPIO18 | IO | VDD_IO_0 | - | - | GPIO18 | I/O/T | GPIO18 | I/O/T | - | - | - | - | - | - | - | - | ADC1_CHANNEL2 | - |
| 20 | GPIO19 | IO | VDD_IO_0 | - | - | GPIO19 | I/O/T | GPIO19 | I/O/T | - | - | - | - | - | - | - | - | ADC1_CHANNEL3 | - |
| 21 | VDD_IO_0 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 22 | GPIO20 | IO | VDD_IO_0 | - | - | GPIO20 | I/O/T | GPIO20 | I/O/T | - | - | - | - | - | - | - | - | ADC1_CHANNEL4 | - |
| 23 | GPIO21 | IO | VDD_IO_0 | - | - | GPIO21 | I/O/T | GPIO21 | I/O/T | - | - | - | - | - | - | - | - | ADC1_CHANNEL5 | - |
| 24 | GPIO22 | IO | VDD_IO_0 | - | - | GPIO22 | I/O/T | GPIO22 | I/O/T | - | - | - | - | - | - | - | - | ADC1_CHANNEL6 | - |
| 25 | GPIO23 | IO | VDD_IO_0 | - | - | GPIO23 | I/O/T | GPIO23 | I/O/T | - | - | REF_SOM_CLK PAD | O | - | - | - | - | ADC1_CHANNEL7 | - |
| 26 | VDD_HP_0 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 27 | FLASH_CS | 专用 | VDD_FLASHIO | - | - | FLASH_CS | O | - | - | - | - | - | - | - | - | - | - | - | - |
| 28 | FLASH_Q | 专用 | VDD_FLASHIO | - | - | FLASH_Q | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 29 | FLASH_WP | 专用 | VDD_FLASHIO | - | - | FLASH_WP | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 30 | VDD_FLASHIO | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 31 | FLASH_HOLD | 专用 | VDD_FLASHIO | - | - | FLASH_HOLD | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 32 | FLASH_CK | 专用 | VDD_FLASHIO | - | - | FLASH_CK | O | - | - | - | - | - | - | - | - | - | - | - | - |
| 33 | FLASH_D | 专用 | VDD_FLASHIO | - | - | FLASH_D | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 34 | DSI_REXT | 专用 | VDD_MIPI_DPHY | - | - | MIPI DSI PHY 4.02 KO EXTER-NAL RESISTOR | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 35 | DSI_DATAPI | 专用 | VDD_MIPI_DPHY | - | - | MIPI DSI PHY DATAP1 | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 36 | DSI_DATANI | 专用 | VDD_MIPI_DPHY | - | - | MIPI DSI PHY DATAN1 | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 37 | DSI_CLKN | 专用 | VDD_MIPI_DPHY | - | - | MIPI DSI PHY CLKN | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 38 | DSI_CLKP | 专用 | VDD_MIPI_DPHY | - | - | MIPI DSI PHY CLKP | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 39 | DSI_DATAPO | 专用 | VDD_MIPI_DPHY | - | - | MIPI DSI PHY DATAP0 | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 40 | DSI_DATANO | 专用 | VDD_MIPI_DPHY | - | - | MIPI DSI PHY DATANO | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 41 | VDD_MIPI_DPHY | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 42 | CSI_DATANO | 专用 | VDD_MIPI_DPHY | - | - | MIPI CSI PHY DATANO | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 43 | CSI_DATAPO | 专用 | VDD_MIPI_DPHY | - | - | MIPI CSI PHY DATAPO | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |

见下页


表 6-1 – 接上页


| 管脚序号 | 管脚名称 | 管脚类型 | 供电管脚 | 管脚配置 | IO MUX 功能 | LP IO MUX 功能 | 模拟功能 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 复位时 | 复位后 | F0 | 类型 | F1 | 类型 | F2 | 类型 | F3 | 类型 | F0 | 类型 | F1 | 类型 | F0 | F1 |
| 44 | CSI_CLKP | 专用 | VDD_MIPDPHY | - | - | MIPI CSI PHYCLKP | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 45 | CSI_CLKN | 专用 | VDD_MIPDPHY | - | - | MIPI CSI PHYCLKN | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 46 | CSI_DATANI | 专用 | VDD_MIPDPHY | - | - | MIPI CSI PHYDATANI | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 47 | CSI_DATAP1 | 专用 | VDD_MIPDPHY | - | - | MIPI CSI PHYDATAP1 | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 48 | CSI_REXT | 专用 | VDD_MIPDPHY | - | - | MIPI CSI PHY4.02 KΩ EXTER-NAL RESISTOR | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 49 | DM | 专用 | VDD_USBPHY | - | - | USB2 OTG PHYDM | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 50 | DP | 专用 | VDD_USBPHY | - | - | USB2 OTG PHYDP | I/O/T | - | - | - | - | - | - | - | - | - | - | - | - |
| 51 | VDD_USBPHY | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 52 | GPIO24 | IO | VDD_IO_4 | - | - | GPIO24 | I/O/T | GPIO24 | I/O/T | - | - | - | - | - | - | - | - | USB1BP1_NO | - |
| 53 | GPIO25 | IO | VDD_IO_4 | - | IE, USB_WPU | GPIO25 | I/O/T | GPIO25 | I/O/T | - | - | - | - | - | - | - | - | USB1BP1_P0 | - |
| 54 | VDD_HP_1 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 55 | GPIO26 | IO | VDD_IO_4 | - | - | GPIO26 | I/O/T | GPIO26 | I/O/T | - | - | - | - | - | - | - | - | USB1BP1_N1 | - |
| 56 | GPIO27 | IO | VDD_IO_4 | - | - | GPIO27 | I/O/T | GPIO27 | I/O/T | - | - | - | - | - | - | - | - | USB1BP1_P1 | - |
| 57 | GPIO28 | IO | VDD_IO_4 | - | - | GPIO28 | I/O/T | GPIO28 | I/O/T | SPI2_CS_pad | I/O/T | GMAC_PHY_RXDV_pad | IO | - | - | - | - | - | - |
| 58 | GPIO29 | IO | VDD_IO_4 | - | - | GPIO29 | I/O/T | GPIO29 | I/O/T | SPI2_D_pad | I/O/T | GMAC_PHY_RXDO_pad | IO | - | - | - | - | - | - |
| 59 | VDD_PSRAM_0 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 60 | GPIO30 | IO | VDD_IO_4 | - | - | GPIO30 | I/O/T | GPIO30 | I/O/T | SPI2_CK_pad | I/O/T | GMAC_PHY_RXD1_pad | IO | - | - | - | - | - | - |
| 61 | GPIO31 | IO | VDD_IO_4 | - | - | GPIO31 | I/O/T | GPIO31 | I/O/T | SPI2_Q_pad | I/O/T | GMAC_PHY_RXER_pad | IO | - | - | - | - | - | - |
| 62 | VDD_IO_4 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 63 | GPIO32 | IO | VDD_IO_4 | IE | - | GPIO32 | I/O/T | GPIO32 | I/O/T | SPI2_HOLDPad | I/O/T | GMAC_RMII_CLK_pad | IO | - | - | - | - | - | - |
| 64 | GPIO33 | IO | VDD_IO_4 | IE | - | GPIO33 | I/O/T | GPIO33 | I/O/T | SPI2_WP_pad | I/O/T | GMAC_PHY_TXEN_pad | O | - | - | - | - | - | - |
| 65 | GPIO34 | IO | VDD_IO_4 | IE | - | GPIO34 | I/O/T | GPIO34 | I/O/T | SPI2_IO4_pad | I/O/T | GMAC_PHY_TXDO_pad | O | - | - | - | - | - | - |
| 66 | GPIO35 | IO | VDD_IO_4 | IE, WPU | - | GPIO35 | I/O/T | GPIO35 | I/O/T | SPI2_IO5_pad | I/O/T | GMAC_PHY_TXDI pad | O | - | - | - | - | - | - |
| 67 | VDD_PSRAM_1 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 68 | GPIO36 | IO | VDD_IO_4 | IE | - | GPIO36 | I/O/T | GPIO36 | I/O/T | SPI2_IO6_pad | I/O/T | GMAC_PHY_TXER_pad | O | - | - | - | - | - | - |
| 69 | GPIO37 | IO | VDD_IO_4 | IE | IE | UARTO_TXD PAD | O | GPIO37 | I/O/T | SPI2_IO7_pad | I/O/T | - | - | - | - | - | - | - | - |
| 70 | GPIO38 | IO | VDD_IO_4 | IE | - | UARTO_RXD PAD | I1 | GPIO38 | I/O/T | SPI2_DQS_pad | O/T | - | - | - | - | - | - | - | - |
| 71 | VDDO_FLASH | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 72 | VDDO_PSRAM | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 73 | VDDO_3 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 74 | VDDO_4 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 75 | VDD_LDO | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 76 | VDD_HP_2 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 77 | VDD_DCDCCC | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 78 | FB_DCDCC | 模拟 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 79 | EN_DCDC | 模拟 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 80 | GPIO39 | IO | VDD_IO_5 | - | - | SD1_CDATAO_pad | I/O/T | GPIO39 | I/O/T | - | - | REF_50M_CLK_pad | O | - | - | - | - | - | - |
| 81 | GPIO40 | IO | VDD_IO_5 | - | - | SD1_CDATAI pad | I/O/T | GPIO40 | I/O/T | - | - | GMAC_PHY_TXEN PAD | O | - | - | - | - | - | - |
| 82 | GPIO41 | IO | VDD_IO_5 | - | - | SD1_CDATAD pad | I/O/T | GPIO41 | I/O/T | - | - | GMAC_PHY_TXDO PAD | O | - | - | - | - | - | - |
| 83 | GPIO42 | IO | VDD_IO_5 | - | - | SD1_CDATAD pad | I/O/T | GPIO42 | I/O/T | - | - | GMAC_PHY_TXDI pad | O | - | - | - | - | - | - |
| 84 | GPIO43 | IO | VDD_IO_5 | - | - | SD1_CCCLK PAD | O | GPIO43 | I/O/T | - | - | GMAC_PHY_TXER PAD | O | - | - | - | - | - | - |
| 85 | VDD_IO_5 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 86 | GPIO44 | IO | VDD_IO_5 | - | - | SD1_CCMD PAD | I/O/T | GPIO44 | I/O/T | - | - | GMAC_RMII_CLK PAD | IO | - | - | - | - | - | - |
| 87 | GPIO45 | IO | VDD_IO_5 | - | - | SD1_CDATAI pad | I/O/T | GPIO45 | I/O/T | - | - | GMAC_PHY_RXDV PAD | IO | - | - | - | - | - | - |
| 88 | GPIO46 | IO | VDD_IO_5 | - | - | SD1_CDATAS pad | I/O/T | GPIO46 | I/O/T | - | - | GMAC_PHY_RXDO PAD | IO | - | - | - | - | - | - |
| 89 | GPIO47 | IO | VDD_IO_5 | - | - | SD1_CDATAG pad | I/O/T | GPIO47 | I/O/T | - | - | GMAC_PHY_RXDI pad | IO | - | - | - | - | - | - |
| 90 | GPIO48 | IO | VDD_IO_5 | - | - | SD1_CDATAD pad | I/O/T | GPIO48 | I/O/T | - | - | GMAC_PHY_RXER PAD | IO | - | - | - | - | - | - |
| 91 | VDD_HP_3 | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 92 | GPIO49 | IO | VDD_IO_6 | - | - | GPIO49 | I/O/T | GPIO49 | I/O/T | - | - | GMAC_PHY_TXEN PAD | O | - | - | - | - | ADC2_CHANNEL10 | - |
| 93 | GPIO50 | IO | VDD_IO_6 | - | - | GPIO50 | I/O/T | GPIO50 | I/O/T | - | - | GMAC_RMII_CLK PAD | IO | - | - | - | - | ADC2_CHANNEL11 | - |
| 94 | GPIO51 | IO | VDD_IO_6 | - | - | GPIO51 | I/O/T | GPIO51 | I/O/T | - | - | GMAC_PHY_RXDV PAD | IO | - | - | - | ADC2_CHANNEL22 | ANA_COMPLOA |  |
| 95 | GPIO52 | IO | VDD_IO_6 | - | - | GPIO52 | I/O/T | GPIO52 | I/O/T | - | - | GMAC_PHY_RXDO PAD | IO | - | - | - | ADC2_CHANNEL3233_COMPLOA |  |  |
| 96 | VDD_IO_6 | 电源 | - |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |


表 6-1 – 接上页


| 管脚序号 | 管脚名称 | 管脚类型 | 供电管脚 | 管脚配置 | IO MUX 功能 | LP IO MUX 功能 | 模拟功能 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 复位时 | 复位后 | F0 | 类型 | F1 | 类型 | F2 | 类型 | F3 | 类型 | F0 | 类型 | F1 | 类型 | F0 | F1 |
| 97 | GPIO53 | IO | VDD_IO_6 | - | - | GPIO53 | I/O/T | GPIO53 | I/O/T | - | - | GMAC_PHY_RXD1PAD | IO | - | - | - | - | ADC2_CHANNEL4 | ANA_COMP1 |
| 98 | GPIO54 | IO | VDD_IO_6 | - | - | GPIO54 | I/O/T | GPIO54 | I/O/T | - | - | GMAC_PHY_RXERPAD | IO | - | - | - | - | ADC2_CHANNEL5 | ANA_COMP1 |
| 99 | XTAL_N | 模拟 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 100 | XTAL_P | 模拟 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 101 | VDD_ANA | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 102 | VDD_BAT | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 103 | CHIP PIO | 模拟 | VDD_BAT | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 104 | GPIOO | IO | VDD_LP/VDD_BAT | - | - | GPIOO | I/O/T | GPIOO | I/O/T | - | - | - | - | LP GPIOO | I/O/T | LP GPIOO | I/O/T | XTAL_32K_N | - |
| 105 | GND | 电源 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |


更多信息详见章节 2 管脚。高亮的单元格，请参考章节 2.3.4 GPIO 和 LP GPIO 的限制。



修订历史


| 日期 | 版本 | 发布说明 |
| --- | --- | --- |
| 2026-03-11 | v0.5 | ESP32-P4芯片版本v3.1预发布 |




# ESPRESSIF

# 免责声明和版权公告

本文档中的信息，包括供参考的 URL 地址，如有变更，恕不另行通知。

本文档可能引用了第三方的信息，所有引用的信息均为“按现状”提供，乐鑫不对信息的准确性、真实性做任何保证。

乐鑫不对本文档的内容做任何保证，包括内容的适销性、是否适用于特定用途，也不提供任何其他乐鑫提案、规格书或样品在他处提到的任何保证。

乐鑫不对本文档是否侵犯第三方权利做任何保证，也不对使用本文档内信息导致的任何侵犯知识产权的行为负责。本文档在此未以禁止反言或其他方式授予任何知识产权许可，不管是明示许可还是暗示许可。

Wi-Fi 联盟成员标志归 Wi-Fi 联盟所有。蓝牙标志是 Bluetooth SIG 的注册商标。

文档中提到的所有商标名称、商标和注册商标均属其各自所有者的财产，特此声明。

版权归 $\circledcirc$ 2026 乐鑫信息科技（上海）股份有限公司。保留所有权利。