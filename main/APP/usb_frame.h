/**
 ******************************************************************************
 * @file        usb_frame.h
 * @version     V1.0
 * @date        2025-01-01
 * @brief       帧缓存操作
 ******************************************************************************
 */

#ifndef __USB_FRAME_H
#define __USB_FRAME_H

#include <string.h>
#include "esp_err.h"
#include "esp_log.h"
#include "esp_check.h"
#include "esp_private/usb_phy.h"
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "driver/jpeg_decode.h"
#include "app_config.h"
#include "tusb_config.h"


/* 函数声明 */
esp_err_t frame_allocate(int nb_of_fb, size_t fb_size);
void frame_reset(frame_t *frame);
esp_err_t frame_return_empty(frame_t *frame);
esp_err_t frame_send_filled(frame_t *frame);
esp_err_t frame_add_data(frame_t *frame, const uint8_t *data, size_t data_len);
frame_t *frame_get_empty(void);
frame_t *frame_get_filled(void);
frame_t *frame_get_filled_tick(TickType_t ticks);

#endif