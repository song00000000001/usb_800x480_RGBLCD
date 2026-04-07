/**
 ******************************************************************************
 * @file        app_hid.h
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       USB HID 驱动
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

#ifndef __APP_HID_H
#define __APP_HID_H

#include "app_config.h"
#include "app_usb.h"
#include "esp_log.h"
#include "esp_check.h"
#include "tusb.h"
#include "device/usbd.h"
#include "tusb_config.h"
#include "usb_descriptors.h"

/* 函数声明 */
esp_err_t app_hid_init(void);
void tinyusb_hid_keyboard_report(hid_report_t report);

#endif
