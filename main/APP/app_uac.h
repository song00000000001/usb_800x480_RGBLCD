/**
 ******************************************************************************
 * @file        app_uac.h
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       USB Audio驱动
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

#ifndef __APP_UAC_H
#define __APP_UAC_H

#include "esp_log.h"
#include "app_config.h"
#include "usb_device_uac.h"
#include "app_usb.h"
#include "es8388.h"
#include "myi2s.h"
#include "xl9555.h"

/* UAC配置参数 */
#define UAC_SPK_INTERVAL_MS    10  /* Speaker数据间隔 */
#define UAC_MIC_INTERVAL_MS    10  /* Microphone数据间隔 */

/* 函数声明 */
esp_err_t app_uac_init(void);

#endif
