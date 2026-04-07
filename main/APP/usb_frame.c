/**
 ******************************************************************************
 * @file        usb_frame.c
 * @version     V1.0
 * @date        2025-01-01
 * @brief       帧缓存操作
 ******************************************************************************
 */

#include "usb_frame.h"

static const char *TAG = "usb_frame";
/* 空帧队形 */
static QueueHandle_t empty_fb_queue = NULL;
/* 填充帧队形 */
static QueueHandle_t filled_fb_queue = NULL;

/**
 * @brief       帧内存申请
 * @param       nb_of_fb:队列可容纳的最大项数
 * @param       fb_size:队列中每个数据项的大小，以字节为单位
 * @retval      0:申请成功，ESP_ERR_NO_MEM:申请内存失败
 */
esp_err_t frame_allocate(int nb_of_fb, size_t fb_size)
{
    esp_err_t ret;
    jpeg_decode_memory_alloc_cfg_t tx_mem_cfg = {
        .buffer_direction = JPEG_DEC_ALLOC_INPUT_BUFFER,
    };

    /* 转递帧缓冲区 */
    empty_fb_queue = xQueueCreate(nb_of_fb, sizeof(frame_t *));
    ESP_RETURN_ON_FALSE(empty_fb_queue, ESP_ERR_NO_MEM, TAG, "Not enough memory for empty_fb_queue %d", nb_of_fb);
    filled_fb_queue = xQueueCreate(nb_of_fb, sizeof(frame_t *));
    ESP_RETURN_ON_FALSE(filled_fb_queue, ESP_ERR_NO_MEM, TAG, "Not enough memory for filled_fb_queue %d", nb_of_fb);

    for (int i = 0; i < nb_of_fb; i++)
    {
        /* 申请帧缓存 */
        frame_t *this_fb = malloc(sizeof(frame_t));
        ESP_RETURN_ON_FALSE(this_fb, ESP_ERR_NO_MEM,  TAG, "Not enough memory for frame buffers %d", fb_size);
        size_t malloc_size = 0;
        uint8_t *this_data = (uint8_t*)jpeg_alloc_decoder_mem(fb_size, &tx_mem_cfg, &malloc_size);

        if (!this_data)
        {
            free(this_fb);
            ret = ESP_ERR_NO_MEM;
            ESP_LOGE(TAG, "Not enough memory for frame buffers %d", fb_size);
        }

        /* 设置默认参数 */
        this_fb->data = this_data;
        this_fb->data_buffer_len = fb_size;
        this_fb->data_len = 0;

        /* 发送空帧队形 */
        const BaseType_t result = xQueueSend(empty_fb_queue, &this_fb, 0);
        assert(pdPASS == result);
    }
    return ret;
}

/**
 * @brief       帧复位
 * @param       frame:图像帧指针
 * @retval      无
 */
void frame_reset(frame_t *frame)
{
    assert(frame);
    frame->data_len = 0;
}

/**
 * @brief       发送空帧队形
 * @param       frame:图像帧指针
 * @retval      ESP_OK:获取成功
 */
esp_err_t frame_return_empty(frame_t *frame)
{
    frame_reset(frame);
    BaseType_t result = xQueueSend(empty_fb_queue, &frame, 0);
    ESP_RETURN_ON_FALSE(result == pdPASS, ESP_ERR_NO_MEM, TAG, "Not enough memory empty_fb_queue");
    return ESP_OK;
}

/**
 * @brief       发送填充帧队形
 * @param       frame:图像帧指针
 * @retval      ESP_OK:获取成功
 */
esp_err_t frame_send_filled(frame_t *frame)
{
    /* 注意：发送到filled队列时不重置，保留数据供显示任务使用 */
    BaseType_t result = xQueueSend(filled_fb_queue, &frame, 0);
    ESP_RETURN_ON_FALSE(result == pdPASS, ESP_ERR_NO_MEM, TAG, "Not enough memory filled_fb_queue");
    return ESP_OK;
}

/**
 * @brief       数据拷贝到帧缓存
 * @param       frame:图像帧指针
 * @param       data:图像数据
 * @param       data_len:图像数据大小
 * @retval      ESP_OK:获取成功
 */
esp_err_t frame_add_data(frame_t *frame, const uint8_t *data, size_t data_len)
{
    ESP_RETURN_ON_FALSE(frame && data && data_len, ESP_ERR_INVALID_ARG, TAG, "Invalid arguments");

    if (frame->data_buffer_len < frame->data_len + data_len)
    {
        ESP_LOGD(TAG, "Frame buffer overflow");
        return ESP_ERR_INVALID_SIZE;
    }
    /* 拷贝数据 */
    memcpy(frame->data + frame->data_len, data, data_len);
    frame->data_len += data_len;
    return ESP_OK;
}

/**
 * @brief       获取一个空的帧队形
 * @param       无
 * @retval      图像帧指针
 */
frame_t *frame_get_empty(void)
{
    frame_t *this_fb;

    if (xQueueReceive(empty_fb_queue, &this_fb, 0) == pdPASS)
    {
        return this_fb;
    }
    else
    {
        return NULL;
    }
}

/**
 * @brief       获取一个填充帧队形
 * @param       无
 * @retval      图像帧指针
 */
frame_t *frame_get_filled(void)
{
    frame_t *this_fb;

    if (xQueueReceive(filled_fb_queue, &this_fb, portMAX_DELAY) == pdPASS)
    {
        return this_fb;
    }
    else
    {
        return NULL;
    }
}

/**
 * @brief       获取一个填充帧队形（带超时）
 * @param       ticks: 超时tick数
 * @retval      图像帧指针，超时返回NULL
 */
frame_t *frame_get_filled_tick(TickType_t ticks)
{
    frame_t *this_fb;

    if (xQueueReceive(filled_fb_queue, &this_fb, ticks) == pdPASS)
    {
        return this_fb;
    }
    else
    {
        return NULL;
    }
}
