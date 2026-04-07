/**
 ****************************************************************************************************
 * @file        rgblcd.c
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       RGBLCD 驱动代码
 * @license     Copyright (c) 2020-2032, 广州市星翼电子科技有限公司
 ****************************************************************************************************
 * @attention
 *
 * 实验平台:正点原子 ESP32-P4 开发板
 * 在线视频:www.yuanzige.com
 * 技术论坛:www.openedv.com
 * 公司网址:www.alientek.com
 * 购买地址:openedv.taobao.com
 *
 ****************************************************************************************************
 */

#include "rgblcd.h"
#include "esp_cache.h"
#include "freertos/task.h"
#include <string.h>


static const char *TAG = "rgblcd";
_rgblcd_dev rgbdev;                         /* 管理RGBLCD重要参数 */
esp_lcd_panel_handle_t panel_handle = NULL; /* RGBLCD句柄 */

/**
 * @brief       初始化RGBLCD
 * @param       无
 * @retval      RGBLCD句柄
 */
esp_lcd_panel_handle_t rgblcd_init(void)
{
    rgbdev.id = lcddev.id;                      /* 读取LCD面板ID */
    /* 配置VDDPST_1管理的IO电压 */
    esp_ldo_channel_handle_t ldo_rgblcd_phy = NULL;
    esp_ldo_channel_config_t ldo_rgblcd_phy_config = {
        .chan_id    = 4,                        /* 选择内存LDO */
        .voltage_mv = 3300,                     /* 输出标准电压提供VDD_RGBLCD_DPHY */
    };
    ESP_ERROR_CHECK(esp_ldo_acquire_channel(&ldo_rgblcd_phy_config, &ldo_rgblcd_phy));

    if (rgbdev.id == 0X4342)                    /* 4.3寸屏, 480*272 RGB屏 */
    {
        rgbdev.pwidth   = 480;                  /* 面板宽度,单位:像素 */
        rgbdev.pheight  = 272;                  /* 面板高度,单位:像素 */
        rgbdev.hsw      = 4;                    /* 水平同步宽度 */
        rgbdev.hbp      = 43;                   /* 水平后廊 */
        rgbdev.hfp      = 8;                    /* 水平前廊 */
        rgbdev.vsw      = 4;                    /* 垂直同步宽度 */
        rgbdev.vbp      = 12;                   /* 垂直后廊 */
        rgbdev.vfp      = 8;                    /* 垂直前廊 */
        rgbdev.pclk_hz  = 9 * 1000 * 1000;      /* 设置像素时钟 9Mhz */
    }
    else if (rgbdev.id == 0X4384)
    {
        rgbdev.pwidth   = 800;                  /* 面板宽度,单位:像素 */
        rgbdev.pheight  = 480;                  /* 面板高度,单位:像素 */
        rgbdev.hsw      = 40;                   /* 水平同步宽度 */
        rgbdev.hbp      = 42;                   /* 水平后廊 - 增加2像素修正偏右问题 */
        rgbdev.hfp      = 48;                   /* 水平前廊 */
        rgbdev.vsw      = 2;                    /* 垂直同步宽度 */
        rgbdev.vbp      = 32;                   /* 垂直后廊 */
        rgbdev.vfp      = 13;                   /* 垂直前廊 */
        rgbdev.pclk_hz  = 30 * 1000 * 1000;     /* 设置像素时钟 30Mhz */
    }
    else if (rgbdev.id == 0X4350)               /* 4.3 寸 800*400 RGB 屏 */
    {
        rgbdev.pwidth   = 800;                  /* 面板宽度，单位：像素 */
        rgbdev.pheight  = 400;                  /* 面板高度，单位：像素 */
        rgbdev.hsw      = 16;                   /* 水平同步宽度 */
        rgbdev.hbp      = 64;                   /* 水平后廊 */
        rgbdev.hfp      = 64;                   /* 水平前廊 */
        rgbdev.vsw      = 4;                    /* 垂直同步宽度 */
        rgbdev.vbp      = 12;                   /* 垂直后廊 */
        rgbdev.vfp      = 8;                    /* 垂直前廊 */
        rgbdev.pclk_hz  = 25 * 1000 * 1000;     /* 设置像素时钟 25Mhz */
    }
    else if (rgbdev.id == 0x7084)               /* ATK-MD0700R-800480 */
    {
        rgbdev.pwidth   = 800;                  /* LCD面板的宽度 */
        rgbdev.pheight  = 480;                  /* LCD面板的高度 */
        rgbdev.hsw      = 1;                    /* 水平同步宽度 */
        rgbdev.hbp      = 48;                   /* 水平后廊 - 增加2像素修正偏右问题 */
        rgbdev.hfp      = 210;                  /* 水平前廊 */
        rgbdev.vsw      = 1;                    /* 垂直同步宽度 */
        rgbdev.vbp      = 23;                   /* 垂直后廊 */
        rgbdev.vfp      = 22;                   /* 垂直前廊 */
        rgbdev.pclk_hz  = 30 * 1000 * 1000;     /* 设置像素时钟 30Mhz */
    }
    else if (rgbdev.id == 0x7016)               /* ATK-MD0700R-1024600 */
    {
        rgbdev.pwidth   = 1024;                 /* LCD面板的宽度 */
        rgbdev.pheight  = 600;                  /* LCD面板的高度 */
        rgbdev.hsw      = 20;                   /* 水平同步宽度 */
        rgbdev.hbp      = 140;                  /* 水平后廊 */
        rgbdev.hfp      = 160;                  /* 水平前廊 */
        rgbdev.vsw      = 3;                    /* 垂直同步宽度 */
        rgbdev.vbp      = 20;                   /* 垂直后廊 */
        rgbdev.vfp      = 12;                   /* 垂直前廊 */
        rgbdev.pclk_hz  = 30 * 1000 * 1000;     /* 设置像素时钟 30Mhz */
    }
    else if (rgbdev.id == 0x1018)               /* ATK-MD1018R-1280800 */
    {
        rgbdev.pwidth   = 1280;                 /* LCD面板的宽度 */
        rgbdev.pheight  = 800;                  /* LCD面板的高度 */
        rgbdev.hsw      = 10;                   /* 水平同步宽度 */
        rgbdev.hbp      = 140;                  /* 水平后廊 */
        rgbdev.hfp      = 10;                   /* 水平前廊 */
        rgbdev.vsw      = 3;                    /* 垂直同步宽度 */
        rgbdev.vbp      = 23;                   /* 垂直后廊 */
        rgbdev.vfp      = 10;                   /* 垂直前廊 */
        rgbdev.pclk_hz  = 48 * 1000 * 1000;     /* 设置像素时钟 48Mhz */
    }

    /* 配置RGB参数 */
    esp_lcd_rgb_panel_config_t panel_config = {     /* RGBLCD配置结构体 */
        .num_fbs            = 1,                    /* 单帧缓冲区 - 解决双缓冲区切换导致的随机偏移 */
        .data_width         = 16,                   /* 数据宽度为16位 */
        .in_color_format    = LCD_COLOR_FMT_RGB565,
        .clk_src            = LCD_CLK_SRC_DEFAULT,  /* RGBLCD外设时钟源 */
        .disp_gpio_num      = GPIO_NUM_NC,          /* 用于显示控制信号,不使用设为-1 */
        .pclk_gpio_num      = GPIO_LCD_PCLK,        /* PCLK信号引脚 */
        .hsync_gpio_num     = GPIO_NUM_NC,          /* HSYNC信号引脚,DE模式可不使用 */
        .vsync_gpio_num     = GPIO_NUM_NC,          /* VSYNC信号引脚,DE模式可不使用 */
        .de_gpio_num        = GPIO_LCD_DE,          /* DE信号引脚 */
        .data_gpio_nums = {                         /* 数据线引脚 */
            GPIO_LCD_B3, GPIO_LCD_B4, GPIO_LCD_B5, GPIO_LCD_B6, GPIO_LCD_B7,
            GPIO_LCD_G2, GPIO_LCD_G3, GPIO_LCD_G4, GPIO_LCD_G5, GPIO_LCD_G6, GPIO_LCD_G7,
            GPIO_LCD_R3, GPIO_LCD_R4, GPIO_LCD_R5, GPIO_LCD_R6, GPIO_LCD_R7,
        },
        .timings = {                                /* RGBLCD时序参数 */
            .pclk_hz            = rgbdev.pclk_hz,   /* 像素时钟频率 */
            .h_res              = rgbdev.pwidth,    /* 水平分辨率,即一行中的像素数 */
            .v_res              = rgbdev.pheight,   /* 垂直分辨率,即帧中的行数 */
            .hsync_back_porch   = rgbdev.hbp,       /* 水平后廊,hsync和行活动数据开始之间的PCLK数 */
            .hsync_front_porch  = rgbdev.hfp,       /* 水平前廊,活动数据结束和下一个hsync之间的PCLK数 */
            .hsync_pulse_width  = rgbdev.hsw,       /* 水平同步宽度,单位:PCLK周期 */
            .vsync_back_porch   = rgbdev.vbp,       /* 垂直后廊,vsync和帧开始之间的无效行数 */
            .vsync_front_porch  = rgbdev.vfp,       /* 垂直前廊,帧结束和下一个vsync之间的无效行数 */
            .vsync_pulse_width  = rgbdev.vsw,       /* 垂直同步宽度,单位:行数 */
            .flags = {
                .pclk_active_neg = true,            /* RGB数据在下降沿计时 */
            },
        },
        .flags.fb_in_psram = true,                  /* 在PSRAM中分配帧缓冲区 */
        .bounce_buffer_size_px = rgbdev.pwidth,     /* Bounce buffer大小为一行像素 - 解决PSRAM延迟导致的DMA同步问题 */
    };

    esp_lcd_new_rgb_panel(&panel_config, &panel_handle);/* 创建RGB对象 */

    /* 在面板初始化前清零帧缓冲区 - 解决每次启动图像随机偏移问题 */
    /* RGB LCD DMA在init后立即启动，如果缓冲区内容随机会导致DE同步失败 */
    void *fb0 = NULL;
    esp_err_t fb_ret = esp_lcd_rgb_panel_get_frame_buffer(panel_handle, 1, &fb0);
    if (fb_ret == ESP_OK && fb0 != NULL) {
        uint32_t fb_size = rgbdev.pwidth * rgbdev.pheight * 2;  /* RGB565: 2 bytes per pixel */
        memset(fb0, 0, fb_size);
        /* 同步缓存确保数据写入内存 */
        esp_cache_msync(fb0, fb_size, ESP_CACHE_MSYNC_FLAG_DIR_C2M | ESP_CACHE_MSYNC_FLAG_UNALIGNED);
        ESP_LOGI(TAG, "Frame buffer cleared before init: FB=%p", fb0);
    }

    ESP_ERROR_CHECK(esp_lcd_panel_reset(panel_handle)); /* 复位RGB屏 */

    ESP_ERROR_CHECK(esp_lcd_panel_init(panel_handle));  /* 初始化RGB */

    /* 等待一帧周期确保DMA与DE信号同步 - DE模式下需要等待首帧完成 */
    vTaskDelay(pdMS_TO_TICKS(50));

    ESP_LOGI(TAG, "RGB LCD initialized: %d x %d @ %d MHz",
             rgbdev.pwidth, rgbdev.pheight, rgbdev.pclk_hz / 1000000);

    rgblcd_display_dir(1);                              /* 设置横屏 */

    return panel_handle;                                /* RGBLCD句柄 */
}

/**
 * @brief       RGBLCD显示方向设置
 * @param       dir:0,竖屏；1,横屏
 * @retval      无
 */
void rgblcd_display_dir(uint8_t dir)
{
    rgbdev.dir = dir;              /* 显示方向 */

    if (rgbdev.dir == 0)           /* 竖屏 */
    {
        rgbdev.width = rgbdev.pheight;
        rgbdev.height = rgbdev.pwidth;
        esp_lcd_panel_swap_xy(panel_handle, true);          /* 交换X和Y轴 */ 
        esp_lcd_panel_mirror(panel_handle, false, true);    /* 对屏幕的Y轴进行镜像处理 */
    }
    else if (rgbdev.dir == 1)      /* 横屏 */
    {
        rgbdev.width = rgbdev.pwidth;
        rgbdev.height = rgbdev.pheight;
        esp_lcd_panel_swap_xy(panel_handle, false);         /* 不需要交换X和Y轴 */
        esp_lcd_panel_mirror(panel_handle, false, false);   /* 对屏幕的XY轴不进行镜像处理 */
    }
    lcddev.width = rgbdev.width;   /* 宽度 */
    lcddev.height = rgbdev.height; /* 高度 */
}
