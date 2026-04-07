/**
 ******************************************************************************
 * @file        app_lcd.c
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       图像帧显示在LCD程序
 * @license     Copyright (c) 2020-2032, 广州市星翼电子科技有限公司
 ******************************************************************************
 * @attention
 *
 * 实验平台:正点原子 ESP32-P4 开发板
 * 在线视频:www.yuanzige.com
 * 技术论坛:www.openedv.com
 * 公司网址:www.alientek.com
 * 购买地址:openedv.taobao.com
 ******************************************************************************
 */

#include "app_lcd.h"
#include "rgblcd.h"
#include "esp_rom_sys.h"
#include "esp_cache.h"
#include "esp_lcd_panel_rgb.h"

static const char *TAG = "app_lcd";
static jpeg_decoder_handle_t jpgd_handle = NULL;
static jpeg_decode_cfg_t decode_cfg = {
    .output_format = JPEG_DECODE_OUT_FORMAT_RGB565,
    .rgb_order = JPEG_DEC_RGB_ELEMENT_ORDER_BGR,
};

/* 单缓冲机制 - 仿main（2）方式，解码完立即显示 */
static uint8_t *jpeg_rx_buf = NULL;
static uint32_t jpeg_buf_size = 0;

/**
 * @brief       lcd初始化
 * @param       无
 * @retval      ESP_OK:初始化成功
 */
esp_err_t app_lcd_init(void)
{
    /* JPEG解码器初始化 */
    jpeg_decode_engine_cfg_t decode_eng_cfg = {
        .intr_priority = 0,
        .timeout_ms = -1,
    };
    ESP_ERROR_CHECK(jpeg_new_decoder_engine(&decode_eng_cfg, &jpgd_handle));

    /* LCD初始化 */
    lcd_init();

    /* 分配单显示缓冲区 - 仿main（2）方式 */
    jpeg_decode_memory_alloc_cfg_t mem_cfg = {
        .buffer_direction = JPEG_DEC_ALLOC_OUTPUT_BUFFER,
    };

    /* JPEG图像实际尺寸为1280x690，解码器按实际尺寸输出(非显示尺寸) */
    /* 需按JPEG实际尺寸分配，并16字节对齐：1280x720 RGB565: 1280*720*2=1843200 */
    size_t buf_size = 1280 * 720 * 2;
    jpeg_buf_size = buf_size;

    jpeg_rx_buf = (uint8_t *)jpeg_alloc_decoder_mem(buf_size, &mem_cfg, (size_t *)&jpeg_buf_size);
    if (jpeg_rx_buf == NULL) {
        ESP_LOGE(TAG, "Failed to allocate JPEG buffer");
        return ESP_ERR_NO_MEM;
    }

    ESP_LOGI(TAG, "JPEG buffer allocated: %p, size=%u", jpeg_rx_buf, (unsigned)jpeg_buf_size);

    return ESP_OK;
}

/**
 * @brief       图像数据显示在LCD上
 * @param       buf:图像数据缓存指针
 * @param       len:图像数据大小
 * @param       width:图像宽度
 * @param       height:图像高度
 * @retval      无
 */
void app_lcd_draw(uint8_t *buf, uint32_t len, uint16_t width, uint16_t height, uint8_t type)
{
    static int fps_count = 0;
    static int64_t start_time = 0;
    fps_count++;
    if (fps_count == 100)
    {
        int64_t end_time = esp_timer_get_time();
        ESP_LOGI(TAG, "Display fps: %.1f", 1000000.0 / ((end_time - start_time) / 100.0));
        start_time = end_time;
        fps_count = 0;
    }

    if (type == UDISP_TYPE_JPG)
    {
        if (len == 0)    /* 帧错误,跳过解码 */
        {
            return;
        }

        uint32_t out_size = 0;
        esp_err_t ret = jpeg_decoder_process(jpgd_handle, &decode_cfg, buf, len,
                                            jpeg_rx_buf, jpeg_buf_size, &out_size);
        if (ret != ESP_OK || out_size == 0)
        {
            ESP_LOGW(TAG, "JPEG decode failed: %s, out_size=%u", esp_err_to_name(ret), (unsigned)out_size);
            return;
        }

        /* 同步缓存 */
        esp_cache_msync(jpeg_rx_buf, out_size, ESP_CACHE_MSYNC_FLAG_DIR_C2M | ESP_CACHE_MSYNC_FLAG_UNALIGNED);

        /* 计算居中绘制的起始坐标 - 仿main（2）方式 */
        int x_offset = (lcddev.width - width) / 2;
        int y_offset = (lcddev.height - height) / 2;

        /* 确保坐标合法性 */
        x_offset = x_offset < 0 ? 0 : x_offset;
        y_offset = y_offset < 0 ? 0 : y_offset;

        /* LCD draw - 解码完立即显示 */
        esp_lcd_panel_draw_bitmap(lcddev.lcd_panel_handle, x_offset, y_offset,
                                  x_offset + width, y_offset + height, jpeg_rx_buf);

        ESP_LOGD(TAG, "JPEG OK: %ux%u -> (%d,%d)", width, height, x_offset, y_offset);
    }
    else if (type == UDISP_TYPE_RGB565)
    {
        uint32_t expected_size = (uint32_t)width * height * 2;
        if (len != expected_size) {
            ESP_LOGW(TAG, "RGB565 size mismatch: %u != %u", len, expected_size);
        }

        /* 同步缓存 */
        esp_cache_msync(buf, len, ESP_CACHE_MSYNC_FLAG_DIR_C2M | ESP_CACHE_MSYNC_FLAG_UNALIGNED);

        /* 计算居中绘制的起始坐标 */
        int x_offset = (lcddev.width - width) / 2;
        int y_offset = (lcddev.height - height) / 2;
        x_offset = x_offset < 0 ? 0 : x_offset;
        y_offset = y_offset < 0 ? 0 : y_offset;

        /* LCD draw */
        esp_lcd_panel_draw_bitmap(lcddev.lcd_panel_handle, x_offset, y_offset,
                                  x_offset + width, y_offset + height, buf);
    }
    else
    {
        ESP_LOGW(TAG, "Unknown type=%d", type);
    }
}