/**
 ******************************************************************************
 * @file        app_lcd.h
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

#ifndef __APP_LCD_H
#define __APP_LCD_H

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "driver/jpeg_decode.h"
#include "app_config.h"
#include "esp_err.h"
#include "esp_timer.h"
#include "lcd.h"

/* 函数声明 */
esp_err_t app_lcd_init(void);
void app_lcd_draw(uint8_t *buf, uint32_t len, uint16_t width, uint16_t height, uint8_t type);

#endif
