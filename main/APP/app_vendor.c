/**
 ******************************************************************************
 * @file        app_vendor.c
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

#include "app_vendor.h"
#include "tusb_config.h"

#if CFG_TUD_VENDOR

static const char *TAG = "app_vendor";
/*  */
static frame_t *current_frame = NULL;
/* 是否正在接收一帧数据（区分"等待帧头"和"正在收数据"） */
static bool receiving_frame = false;
/* 进度日志上次打印的进度百分比 */
static uint32_t last_progress_percent = 0;
/* 帧头跨包缓存 */
static uint8_t header_cache[USB_FRAME_HEADER_SIZE];
static int header_cache_len = 0;
/* 跳过无效帧数据的剩余字节数（dimension mismatch时payload未完整的情况） */
static uint32_t skip_remaining = 0;

/**
 * @brief       计算CRC16校验（MODBUS标准）
 * @param       data:数据指针
 * @param       len:数据长度
 * @retval      CRC16值
 */
static uint16_t calculate_crc16(const uint8_t *data, size_t len)
{
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++)
    {
        crc ^= data[i];
        for (int j = 0; j < 8; j++)
        {
            if (crc & 1)
            {
                crc = (crc >> 1) ^ 0xA001;
            }
            else
            {
                crc >>= 1;
            }
        }
    }
    return crc;
}

/**
 * @brief       验证帧头CRC
 * @param       header:帧头指针
 * @retval      true:校验通过，false:校验失败
 */
static bool validate_header_crc(const udisp_frame_header_t *header)
{
    /* 帧头结构：CRC16(2字节) + 数据(14字节) */
    /* CRC校验的是从type开始到最后的14字节数据 */
    const uint8_t *data = (const uint8_t *)header + 2;  /* 跳过CRC字段 */
    uint16_t calculated_crc = calculate_crc16(data, 14);
    return (calculated_crc == header->crc16);
}


/**
 * @brief       传输任务
 * @param       pvParameter:未使用传参
 * @retval      ESP_OK:初始化成功，其他为初始化失败
 */
void transfer_task(void *pvParameter)
{
    pvParameter = pvParameter;
    /* 申请32个帧缓存以应对高帧率持续传输 */
    frame_allocate(32, JPEG_BUFFER_SIZE);
    frame_t *usr_frame = NULL;

    while (1)
    {
        /* 等待完整帧 - 帧完成时 buffer_fill 会发送到 filled 队列 */
        usr_frame = frame_get_filled();
        if (usr_frame != NULL)
        {
            ESP_LOGD(TAG, "transfer_task: got COMPLETE frame, type=%d, total=%u",
                     usr_frame->type, (unsigned)usr_frame->info.total);
            app_lcd_draw(usr_frame->data, usr_frame->info.total,
                         usr_frame->info.width, usr_frame->info.height, usr_frame->type);
            frame_return_empty(usr_frame);
        }
    }
}

/**
 * @brief       缓存填充
 * @param       frame:图像帧指针
 * @param       buf:图像缓存指针
 * @param       len:一帧图像大小
 * @retval      >0: 本次填充的字节数，帧可能完成；0: 无数据填充
 */
static int buffer_fill(frame_t *frame, uint8_t *buf, uint32_t len)
{
    if (0 == len || NULL == frame || NULL == buf)
    {
        return 0;
    }

    /* 计算还需要多少数据来完成帧 */
    uint32_t remaining = frame->info.total - frame->info.received;
    uint32_t to_fill = (len < remaining) ? len : remaining;

    /* 拷贝数据 */
    if (to_fill > 0)
    {
        if (frame_add_data(frame, buf, to_fill) != ESP_OK)
        {
            ESP_LOGE(TAG, "buffer_fill: buf overflow!");
            return 0;
        }
        frame->info.received += to_fill;
    }

    /* 每50%进度打印一次 */
    uint32_t progress_percent = (frame->info.received * 100) / frame->info.total;
    if (progress_percent / 50 > last_progress_percent / 50)
    {
        ESP_LOGD(TAG, "RX: %u%% (%u/%u bytes)",
                 progress_percent,
                 (unsigned)frame->info.received,
                 (unsigned)frame->info.total);
        last_progress_percent = progress_percent;
    }

    /* 检查帧是否完成 */
    if (frame->info.received >= frame->info.total)
    {
        last_progress_percent = 0;
        frame_send_filled(frame);
    }

    return (int)to_fill;
}

/**
 * @brief       缓存填充
 * @param       frame:图像帧指针
 * @param       buf:图像缓存指针
 * @param       len:一帧图像大小
 * @retval      true:填充成功，false:填充失败
 */
void tud_vendor_rx_cb(uint8_t itf)
{
    /* 接收缓存 - 使用静态缓冲区避免频繁分配 */
    static uint8_t rx_buf[USB_VENDOR_RX_BUFSIZE * 2];  /* 加倍大小以防帧头跨包 */

    /* 判断是否无效 */
    while (tud_vendor_n_available(itf))
    {
        /* 读取数据到缓存末尾（如果有之前缓存的帧头部分） */
        int offset = header_cache_len;
        int read_res = tud_vendor_n_read(itf, rx_buf + offset, USB_VENDOR_RX_BUFSIZE);

        ESP_LOGD(TAG, "USB callback: read %d bytes, offset=%d, total=%d, receiving=%d",
                 read_res, offset, read_res + offset, receiving_frame);

        if (read_res > 0)
        {
            read_res += offset;  /* 总有效数据长度 */
            header_cache_len = 0;  /* 重置缓存计数 */

            /* 关键变量：跟踪当前数据包中已处理的位置 */
            int processed = 0;

            /* 循环处理数据包中的所有数据（可能包含帧结束和新帧头） */
            while (processed < read_res)
            {
                if (!receiving_frame)
                {
                    /* 先处理跨包跳过的数据（dimension mismatch时payload未完整的情况） */
                    if (skip_remaining > 0)
                    {
                        int remaining = read_res - processed;
                        if (remaining > 0)
                        {
                            uint32_t skip = (remaining < skip_remaining) ? remaining : skip_remaining;
                            processed += skip;
                            skip_remaining -= skip;
                            ESP_LOGD(TAG, "RX: skip_remaining=%u, skipped %u bytes", skip_remaining + skip, skip);
                        }
                        if (skip_remaining > 0)
                        {
                            /* 还有数据要跳过，break等待下一包 */
                            break;
                        }
                        /* skip_remaining == 0, 继续处理正常逻辑 */
                    }

                    /* 等待帧头状态 - 搜索同步标记 */
                    int remaining = read_res - processed;

                    /* 需要至少4字节来搜索同步标记 */
                    if (remaining < UDISP_SYNC_MARKER_LEN)
                    {
                        /* 数据不足，缓存剩余数据等待下一个数据包 */
                        if (remaining > 0)
                        {
                            memmove(rx_buf, rx_buf + processed, remaining);
                            header_cache_len = remaining;
                        }
                        break;
                    }

                    /* 搜索同步标记 "UDSP" - 只在缓冲区起始位置查找，防止在payload中误匹配 */
                    uint8_t *data_ptr = rx_buf + processed;
                    int sync_pos = -1;

                    /* 关键修复：只在位置0查找同步标记，不要在整个数据中搜索
                     * 原因：JPEG等压缩数据的字节序列可能包含"UDSP"，导致误匹配
                     * 新帧的同步标记一定在USB数据包的开头（如果不在前一包的header_cache中）*/
                    if (remaining >= UDISP_SYNC_MARKER_LEN &&
                        memcmp(data_ptr, UDISP_SYNC_MARKER, UDISP_SYNC_MARKER_LEN) == 0)
                    {
                        sync_pos = 0;
                    }

                    if (sync_pos < 0)
                    {
                        /* 未找到同步标记，缓存最后3字节以防同步标记跨包 */
                        if (remaining > 0)
                        {
                            memmove(rx_buf, rx_buf + processed + remaining - 3, 3);
                            header_cache_len = 3;
                        }
                        break;
                    }

                    /* 找到同步标记，跳到同步位置 */
                    processed += sync_pos;

                    /* 检查是否有完整的帧头 */
                    remaining = read_res - processed;
                    if (remaining < USB_FRAME_HEADER_SIZE)
                    {
                        /* 帧头不完整，缓存剩余数据 */
                        if (remaining > 0)
                        {
                            memmove(rx_buf, rx_buf + processed, remaining);
                            header_cache_len = remaining;
                        }
                        break;
                    }

                    udisp_frame_header_t *pblt = (udisp_frame_header_t *)(rx_buf + processed);

                    /* 判断数据类型 */
                    switch (pblt->type)
                    {
                        case UDISP_TYPE_RGB565:
                        case UDISP_TYPE_RGB888:
                        case UDISP_TYPE_YUV420:
                        case UDISP_TYPE_JPG:
                        {
                            /* 判断是否所需要的数据 */
                            if (pblt->x != 0 || pblt->y != 0 || pblt->width != lcddev.width || pblt->height != lcddev.height)
                            {
                                ESP_LOGD(TAG, "RX: sync found at %d, type=%d, width=%d, height=%d, payload=%u",
                                         sync_pos, pblt->type, pblt->width, pblt->height, pblt->payload_total);
                                ESP_LOGD(TAG, "RX: first 20 bytes: %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x",
                                         rx_buf[processed], rx_buf[processed+1], rx_buf[processed+2], rx_buf[processed+3],
                                         rx_buf[processed+4], rx_buf[processed+5], rx_buf[processed+6], rx_buf[processed+7],
                                         rx_buf[processed+8], rx_buf[processed+9], rx_buf[processed+10], rx_buf[processed+11],
                                         rx_buf[processed+12], rx_buf[processed+13], rx_buf[processed+14], rx_buf[processed+15],
                                         rx_buf[processed+16], rx_buf[processed+17], rx_buf[processed+18], rx_buf[processed+19]);
                                ESP_LOGD(TAG, "RX: dimension mismatch, dropping");

                                /* 修复bug: 需要跳过整个帧(header+payload)，而不是只跳过header
                                 * 否则payload数据残留在buffer中，导致后续帧的sync marker检测错误 */
                                uint32_t frame_size = USB_FRAME_HEADER_SIZE + pblt->payload_total;
                                processed += USB_FRAME_HEADER_SIZE;  /* 先跳过header */

                                /* 检查payload是否在当前buffer中 */
                                remaining = read_res - processed;
                                if (pblt->payload_total > remaining)
                                {
                                    /* payload数据跨多包，设置skip_remaining并在当前buffer中跳过已有的数据 */
                                    ESP_LOGD(TAG, "RX: frame payload spans multiple packets, skip_remaining=%u", pblt->payload_total - remaining);
                                    skip_remaining = pblt->payload_total - remaining;
                                    /* 跳过当前buffer中已有的payload数据 */
                                    processed += remaining;
                                    /* 继续处理剩余数据（可能导致processed >= read_res，退出while循环） */
                                    continue;
                                }

                                /* 跳过完整的payload数据 */
                                processed += pblt->payload_total;
                                ESP_LOGD(TAG, "RX: dropped full frame, skipped %u bytes total", frame_size);
                                continue;  /* 继续处理buffer中剩余的数据（可能有下一帧） */
                            }

                            static int fps_count = 0;
                            static int64_t start_time = 0;
                            fps_count++;

                            if (fps_count == 100)
                            {
                                int64_t end_time = esp_timer_get_time();
                                ESP_LOGI(TAG, "Input fps: %.2f", 1000000.0 / ((end_time - start_time) / 100.0));
                                start_time = end_time;
                                fps_count = 0;
                            }
                            /* 获取一个空的帧缓存 */
                            current_frame = frame_get_empty();

                            if (current_frame)
                            {
                                receiving_frame = true;
                                last_progress_percent = 0;  /* 重置进度日志 */
                                current_frame->type = pblt->type;
                                current_frame->info.width = pblt->width;
                                current_frame->info.height = pblt->height;
                                current_frame->info.total = pblt->payload_total;
                                current_frame->info.received = 0;

                                /* 跳过帧头，处理帧头后面的数据 */
                                processed += USB_FRAME_HEADER_SIZE;
                            }
                            else
                            {
                                ESP_LOGE(TAG, "Get frame is null - frame buffer exhausted, skipping frame");
                                receiving_frame = false;
                                current_frame = NULL;
                                processed += USB_FRAME_HEADER_SIZE;  /* 跳过这个帧头 */
                            }
                            break;
                        }
                        default:
                            ESP_LOGW(TAG, "RX: unknown type=%d", pblt->type);
                            processed += USB_FRAME_HEADER_SIZE;  /* 跳过无效帧头 */
                            break;
                    }
                }
                else
                {
                    /* 正在接收帧数据状态 */
                    int data_len = read_res - processed;
                    int filled = buffer_fill(current_frame, rx_buf + processed, data_len);

                    if (filled > 0)
                    {
                        processed += filled;

                        /* 检查帧是否完成 */
                        if (current_frame->info.received >= current_frame->info.total)
                        {
                            /* 帧完成，重置状态，继续处理剩余数据（可能包含新帧头） */
                            current_frame = NULL;
                            receiving_frame = false;
                        }
                    }
                    else
                    {
                        /* 填充失败，跳过这个数据 */
                        processed += 1;
                    }
                }
            }
        }
    }
}

/**
 * @brief       USB OTG初始化
 * @param       无
 * @retval      ESP_OK:初始化成功，其他为初始化失败
 */
esp_err_t app_vendor_init(void)
{
    xTaskCreatePinnedToCore(transfer_task, "transfer_task", 4096, NULL, VENDOR_TASK_PRIORITY, NULL, 0);
    return ESP_OK;
}

#else /* CFG_TUD_VENDOR */

/* Vendor 模式未启用时的空实现 */

esp_err_t app_vendor_init(void)
{
    return ESP_OK;
}

#endif /* CFG_TUD_VENDOR */