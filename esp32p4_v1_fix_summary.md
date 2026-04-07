# ESP32-P4 v1.0 UVC 项目修复总结

## 项目概述

这是一个基于 ESP32-P4 的 USB UVC 显示项目，目标是通过 USB 将 LCD 显示内容作为视频流传输到 Linux 主机。

---

## 主要修复内容

### 1. ESP32-P4 v1.0 芯片兼容性配置

**问题现象**:
- 烧录失败：`'bootloader/bootloader.bin' requires chip revision in range [v3.1 - v3.99]`
- 时钟初始化失败：`assert failed: esp_clk_init clk.c:103`
- PSRAM 初始化崩溃：`Guru Meditation Error: Core 0 panic'ed`
- 帧缓冲区分配失败：`lcd_rgb_panel_alloc_frame_buffers: no mem for frame buffer`

**修复方案** (修改 sdkconfig):

```ini
# 芯片版本支持
CONFIG_ESP32P4_REV_MIN_0=y
CONFIG_ESP_REV_MIN_FULL=0
CONFIG_ESP32P4_SELECTS_REV_LESS_V3=y

# CPU 频率 (v1.0 最高 360MHz)
CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_360=y
CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ=360

# PSRAM 配置
CONFIG_SPIRAM=y
CONFIG_SPIRAM_MODE_HEX=y
CONFIG_SPIRAM_SPEED_80M=y
CONFIG_SPIRAM_BOOT_INIT=y
CONFIG_SPIRAM_MEMTEST=y
CONFIG_SPIRAM_USE_MALLOC=y
CONFIG_SPIRAM_ALLOW_BSS_SEG_EXTERNAL_MEMORY=y
```

---

### 2. UVC 视频格式修改

**问题**: Linux 内核报错 `Cannot allocate memory`

**修复**: 将 MJPEG 格式改为 YUY2 未压缩格式

**修改文件**: `main/APP/usb_descriptors.c`

```c
/* VS 描述符使用 YUY2 未压缩格式 */
#define VS_FRAME_LEN  TUD_VIDEO_DESC_CS_VS_FRM_UNCOMPR_CONT_LEN
#define VS_DESC_LEN   (TUD_VIDEO_DESC_CS_VS_FMT_UNCOMPR_LEN + VS_FRAME_LEN + TUD_VIDEO_DESC_CS_VS_COLOR_MATCHING_LEN)

/* 描述符内容 */
TUD_VIDEO_DESC_CS_VS_FMT_UNCOMPR(1, 1, TUD_VIDEO_GUID_YUY2, 16, 1, 0, 0, 0, 0),
TUD_VIDEO_DESC_CS_VS_FRM_UNCOMPR_CONT(1, 0, 800, 400,
    800*400*16*30, 800*400*16*30, 800*400*2, 333333, 333333, 333333, 1),
TUD_VIDEO_DESC_CS_VS_COLOR_MATCHING(1, 1, 1),
```

---

### 3. UVC 应用层修复

**修改文件**: `main/APP/uvc_app.c`

#### 3.1 添加 RGB565 到 YUY2 转换

```c
static void rgb565_to_yuy2(const uint16_t *rgb565, uint8_t *yuy2, uint32_t pixels)
{
    for (uint32_t i = 0; i < pixels; i += 2) {
        // RGB565 提取并扩展到 8 位
        // 使用 ITU-R BT.601 转换公式
        uint8_t y1 = (66 * r1 + 129 * g1 + 25 * b1 + 128) >> 8;
        uint8_t y2 = (66 * r2 + 129 * g2 + 25 * b2 + 128) >> 8;
        uint8_t u = (-38 * r1 - 74 * g1 + 112 * b1 + 128 + (-38 * r2 - 74 * g2 + 112 * b2 + 128)) >> 9;
        uint8_t v = (112 * r1 - 94 * g1 - 18 * b1 + 128 + (112 * r2 - 94 * g2 - 18 * b2 + 128)) >> 9;
        // YUY2 格式: Y0 U0 Y1 V0
        yuy2[i * 2] = y1;
        yuy2[i * 2 + 1] = u;
        yuy2[i * 2 + 2] = y2;
        yuy2[i * 2 + 3] = v;
    }
}
```

#### 3.2 修复帧缓冲区类型

```c
// 修改前: uint8_t *lcd_fb[3] = {NULL, NULL, NULL};
// 修改后: void *lcd_fb[3] = {NULL, NULL, NULL};
```

#### 3.3 修复 TinyUSB 回调

**关键修复**: TinyUSB 没有 `tud_video_stream_started_cb` 等回调函数，streaming 状态必须在 `tud_video_probe_commit_cb` 中设置：

```c
int tud_video_probe_commit_cb(uint_fast8_t ctl_idx, uint_fast8_t stm_idx,
                              video_probe_and_commit_control_t const *parameters)
{
    s_uvc_status.format_index = parameters->bFormatIndex;
    s_uvc_status.frame_index = parameters->bFrameIndex;
    s_uvc_status.max_frame_size = parameters->dwMaxVideoFrameSize;

    // 关键：commit 后设置 streaming 状态为 true
    s_uvc_status.streaming = true;
    s_uvc_status.connected = true;
    ESP_LOGI(TAG, "UVC 流已提交，准备传输");

    (void)ctl_idx;
    (void)stm_idx;
    return VIDEO_ERROR_NONE;
}
```

---

## 测试方法

编译并烧录：
```bash
idf.py build flash monitor
```

在 Linux 上测试：
```bash
# 查看设备
lsusb
# 应看到：ID 303a:2986 Espressif Systems DNESP32-P4 Board

# 查看视频设备
ls -l /dev/video*

# 使用 ffplay 测试
ffplay -f v4l2 -input_format yuyv422 -video_size 800x400 -framerate 30 /dev/video0

# 或使用 VLC
vlc v4l2:///dev/video0
```

---

## 技术要点总结

| 问题 | 根因 | 解决方案 |
|------|------|----------|
| Bootloader 版本不匹配 | 默认配置要求 v3.1+ 芯片 | 设置 `CONFIG_ESP_REV_MIN_FULL=0` |
| CPU 频率失败 | v1.0 不支持 400MHz | 设置 360MHz |
| PSRAM 初始化崩溃 | v1.0 PSRAM 不稳定 | 降低到 80MHz，启用 boot init |
| 帧缓冲分配失败 | PSRAM malloc 未启用 | 启用 SPIRAM_USE_MALLOC |
| UVC 无法分配内存 | MJPEG 格式问题 | 改用 YUY2 未压缩格式 |
| 视频流不启动 | 错误的 TinyUSB 回调 | 在 probe_commit 中设置 streaming |

---

## 参考资料

- ESP-IDF 版本: v6.1
- 开发板: 正点原子 ESP32-P4 开发板
- LCD: 1024x600 RGB 接口 (实际 UVC 输出 800x400)
- PSRAM: 32MB Hex PSRAM

---

## 待完成事项

- 重新烧录最新代码并测试视频流
- 验证 Linux 上 ffplay/VLC 能正常播放
- 如仍有问题，可能需要检查帧传输时序