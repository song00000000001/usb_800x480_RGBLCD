/**
 ******************************************************************************
 * @file        app_vendor.h
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       USB OTG数据获取
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

#ifndef __APP_VENDOR_H
#define __APP_VENDOR_H

#include <string.h>
#include "app_config.h"
#include "device/usbd.h"
#include "esp_log.h"
#include "esp_err.h"
#include "usb_frame.h"
#include "esp_timer.h"
#include "app_lcd.h"
#include "tusb.h"

/* 函数声明 */
esp_err_t app_vendor_init(void);

#endif
