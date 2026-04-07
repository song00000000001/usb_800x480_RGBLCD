# 成员B 工作内容与流程文档

## 基本信息

| 项目 | 内容 |
|------|------|
| **代号** | 帧控师 (Frame Architect) |
| **角色** | 显示子系统负责人 |
| **技术领域** | LCD驱动、JPEG解码、帧缓冲管理、图像处理 |

---

## 一、核心职责

### 1.1 显示子系统
- RGB LCD驱动开发和维护
- 多面板自动识别支持（7种面板ID）
- JPEG解码和显示输出
- 帧缓冲管理和优化

### 1.2 图像处理
- 硬件JPEG解码
- 像素格式转换（BGR565）
- 显示输出时序控制

---

## 二、工作流程

### 2.1 LCD初始化流程

```
app_lcd_init()
│
├── lcd_init()                 # LCD底层初始化
├── lcd Identification()       # 面板ID识别
├── esp_lcd_new_rgb_panel()    # 创建RGB面板
├── esp_lcd_panel_init()       # 面板初始化
├── esp_lcd_panel_draw_bitmap() # 绘制测试图像
└── jpeg_decoder_init()        # JPEG解码器初始化
```

### 2.2 帧数据传输流程

```
transfer_task()
│
├── frame_get_filled()         # 等待完整帧
└── app_lcd_draw()            # 显示帧
    ├── jpeg_decoder_process() # JPEG解码
    └── esp_lcd_panel_draw_bitmap()  # 刷屏
```

### 2.3 面板识别映射表

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

## 三、关键代码模块

| 文件 | 功能 |
|------|------|
| `main/APP/app_lcd.c` | LCD应用层、JPEG解码 |
| `main/APP/usb_frame.c` | 帧缓冲管理 |
| `components/BSP/LCD/lcd.c` | LCD底层驱动 |
| `components/BSP/LCD/rgblcd.c` | RGB LCD驱动 |
| `components/BSP/LCD/mipi_lcd.c` | MIPI LCD驱动 |
| `components/BSP/LCD/lcdfont.h` | LCD字库 |

---

## 四、帧缓冲管理架构

### 4.1 双缓冲机制
```
frame_allocate(8, JPEG_BUFFER_SIZE)
│
├── xQueueCreate(empty_fb_queue, 8)   # 空缓冲队列
├── xQueueCreate(filled_fb_queue, 8)  # 满缓冲队列
└── 8x frame_t allocated
```

### 4.2 帧数据结构
```c
typedef struct {
    uint8_t *buf;          // 缓冲区指针
    size_t size;           // 缓冲区大小
    uint32_t width;        // 帧宽度
    uint32_t height;       // 帧高度
    uint8_t type;          // 数据类型 (RGB565/JPEG/YUV420)
    uint32_t frame_id;     // 帧ID
} frame_t;
```

---

## 五、预期挑战与解决方案

### 挑战1：LCD颜色显示错误

**问题描述**：
- 颜色显示偏红/偏蓝
- 颜色与预期不符

**原因**：像素格式配置错误，固件期望**BGR565**而非RGB565

**解决方案**：
- PC端发送时转换RGB为BGR：
```c
const b5 = (color.b >> 3) & 0x1F
const g6 = (color.g >> 2) & 0x3F
const r5 = (color.r >> 3) & 0x1F
const bgr565 = (b5 << 11) | (g6 << 5) | r5
```
- 检查LCD驱动中的像素格式配置
- 验证帧头中type字段设置

### 挑战2：JPEG解码失败或花屏

**问题描述**：
- JPEG图像解码后显示异常
- 画面出现条纹/杂色

**解决方案**：
- 验证JPEG数据完整性（检查CRC）
- 确认JPEG解码器缓冲区大小（768000字节）
- 检查JPEG硬件解码器初始化
- 验证JPEG质量参数配置

### 挑战3：帧撕裂或显示不连续

**问题描述**：
- 画面出现撕裂线
- 帧显示不连贯

**原因**：单缓冲机制在写入时覆盖正在显示的帧

**解决方案**：
- 使用双缓冲或多缓冲机制
- 当前已实现8帧缓冲池
- 确保frame_send_filled()在显示完成后才释放缓冲
- 检查VSYNC信号时序

### 挑战4：多面板兼容性问题

**问题描述**：
- 部分面板无法识别
- 分辨率不匹配导致显示异常

**解决方案**：
- 实现自动检测面板ID
- 针对不同分辨率调整时序参数
- 扩展面板ID识别表支持更多型号
- 保留MIPI LCD作为备用方案

### 挑战5：高分辨率帧率低

**问题描述**：
- 1280x800分辨率帧率低
- JPEG解码成为瓶颈

**解决方案**：
- 启用硬件JPEG解码（已实现）
- 调整JPEG压缩质量
- 考虑局部刷新策略
- 优化帧缓冲队列管理

---

## 六、调试方法

### 6.1 串口日志输出
```
I (900) app_lcd: JPEG buffer allocated: 0x70000000, size=768000
I (950) transfer_task: Input fps: 15.32
I (1000) app_lcd: Display fps: 15.28
```

### 6.2 帧率计算公式
```
Display FPS = 1 / (JPEG解码时间 + LCD刷屏时间)
```

### 6.3 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 全白/全黑画面 | 背光未开启或GPIO配置错误 | 检查GPIO53背光控制 |
| 颜色偏斜 | BGR/RGB格式错误 | 转换像素格式为BGR565 |
| JPEG花屏 | 数据损坏或解码器错误 | 检查CRC校验 |
| 撕裂 | 缓冲机制不完善 | 启用双缓冲 |

---

## 七、GPIO资源分配

| GPIO | 功能 | 说明 |
|------|------|------|
| GPIO3-22 | RGB LCD数据线 | 24位数据总线 |
| GPIO20 | LCD PCLK | 像素时钟 |
| GPIO22 | LCD DE | 数据使能 |
| GPIO52 | LCD RST | 复位信号 |
| GPIO53 | LCD背光 | 背光控制 |

---

## 八、交接检查清单

### 8.1 功能验证
- [ ] 多面板自动识别正常
- [ ] JPEG解码显示正常
- [ ] 帧率稳定在15fps以上
- [ ] 无撕裂/闪烁现象

### 8.2 性能指标
- [ ] 800x480分辨率：15-30fps
- [ ] JPEG缓冲区充足（768KB）
- [ ] 帧延迟<100ms

---

> **文档版本**: V1.0
> **创建日期**: 2026-04-02
> **维护人**: 成员B (帧控师)
