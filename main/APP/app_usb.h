/**
 ******************************************************************************
 * @file        app_usb.h
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       USB总线配置
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

#ifndef __APP_USB_H
#define __APP_USB_H

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_private/usb_phy.h"
#include "usb_descriptors.h"
#include "device/usbd.h"
#include "app_config.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_check.h"
#include "app_vendor.h"
#include "app_hid.h"
#include "app_uac.h"
#include <stdint.h>

/* 函数声明 */
esp_err_t app_usb_init(void);

#endif
