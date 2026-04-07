/**
 ******************************************************************************
 * @file        app_hid.c
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

#include "app_hid.h"

static const char *TAG = "tinyusb_hid.h";

typedef struct {
    TaskHandle_t task_handle;
    QueueHandle_t hid_queue;
} tinyusb_hid_t;

static tinyusb_hid_t *s_tinyusb_hid = NULL;

#if CFG_TUD_HID
/**
 * @brief       HID回调函数
 * @param       report:HID 信息
 * @retval      无
 */
void tinyusb_hid_keyboard_report(hid_report_t report)
{
    /* 检查设备是否挂起？ */
    if (tud_suspended())
    {
        /* 远程唤醒 */
        tud_remote_wakeup();
    }
    else
    {
        xQueueSend(s_tinyusb_hid->hid_queue, &report, 0);
    }
}

/**
 * @brief       HID任务函数
 * @param       arg:未使用
 * @retval      无
 */
static void tinyusb_hid_task(void *arg)
{
    (void) arg;
    hid_report_t report;

    while (1)
    {
        if (xQueueReceive(s_tinyusb_hid->hid_queue, &report, portMAX_DELAY)) {
            /* 检查设备是否挂起？ */
            if (tud_suspended())
            {
                /* 远程唤醒 */
                tud_remote_wakeup();
                xQueueReset(s_tinyusb_hid->hid_queue);
            }
            else
            {
                /* 触摸报文 - 已禁用 */
                /* TODO: 其他报文处理 */
                continue;
                /* 等待报文发送完成 */
                if (!ulTaskNotifyTake(pdTRUE, pdMS_TO_TICKS(100)))
                {
                    ESP_LOGW(TAG, "Report not sent");
                }
            }
        }
    }
}
#endif

/**
 * @brief       HID初始化
 * @param       无
 * @retval      ESP_OK:初始化成功
 */
esp_err_t app_hid_init(void)
{
    if (s_tinyusb_hid)
    {
        ESP_LOGW(TAG, "tinyusb_hid already initialized");
        return ESP_OK;
    }

    esp_err_t ret = ESP_OK;
    s_tinyusb_hid = calloc(1, sizeof(tinyusb_hid_t));
    ESP_RETURN_ON_FALSE(s_tinyusb_hid, ESP_ERR_NO_MEM, TAG, "calloc failed");
    s_tinyusb_hid->hid_queue = xQueueCreate(10, sizeof(hid_report_t));   /* 根据您的需求调整队列长度和项目大小 */
    ESP_GOTO_ON_FALSE(s_tinyusb_hid->hid_queue, ESP_ERR_NO_MEM, fail, TAG, "xQueueCreate failed");

    xTaskCreate(tinyusb_hid_task, "tinyusb_hid_task", 4096, NULL, HID_TASK_PRIORITY, &s_tinyusb_hid->task_handle);
    /* 确保 tinyusb_hid_task 创建成功 */
    ESP_GOTO_ON_FALSE(s_tinyusb_hid->task_handle, ESP_ERR_NO_MEM, fail, TAG, "xQueueCreate failed");
    xTaskNotifyGive(s_tinyusb_hid->task_handle);
    return ESP_OK;
fail:
    free(s_tinyusb_hid);
    s_tinyusb_hid = NULL;
    return ret;
}

/**
 * @brief       成功向主机发送报文时调用(注意：对于综合报文，report[0] 是报文编号)
 * @param       itf:未使用
 * @param       report:未使用
 * @param       len:未使用
 * @retval      应用程序可以使用此功能发送下一份报文
 */
void tud_hid_report_complete_cb(uint8_t itf, uint8_t const *report, uint16_t len)
{
    (void) itf;
    (void) len;
    xTaskNotifyGive(s_tinyusb_hid->task_handle);
}

/**
 * @brief       收到GET_REPORT控制请求时调用
 * @param       itf:未使用
 * @param       report_id:报文ID
 * @param       report_type:报文类型
 * @param       buffer:报文内容
 * @param       reqlen:报文大小
 * @retval      应用程序必须填充缓冲报文的内容并返回其长度
 */
uint16_t tud_hid_get_report_cb(uint8_t itf, uint8_t report_id, hid_report_type_t report_type, uint8_t *buffer, uint16_t reqlen)
{
    /* 待办事项未实现 */
    (void) itf;
    (void) report_id;
    (void) report_type;
    (void) buffer;
    (void) reqlen;

    return 0;
}

/**
 * @brief       收到设置报告控制请求或在OUT端点收到数据时调用（报告ID=0，类型=0）
 * @param       itf:未使用
 * @param       report_id:报文ID
 * @param       report_type:报文类型
 * @param       buffer:报文内容
 * @param       reqlen:报文大小
 * @retval      无
 */
void tud_hid_set_report_cb(uint8_t itf, uint8_t report_id, hid_report_type_t report_type, uint8_t const *buffer, uint16_t bufsize)
{
    /* TODO set LED based on CAPLOCK, NUMLOCK etc... */
    (void) itf;
    (void) report_id;
    (void) report_type;
    (void) buffer;
    (void) bufsize;

    switch (report_id)
    {
        default:
        {
            break;
        }
    }
}
