/**
 ******************************************************************************
 * @file        app_usb.c
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

#include "app_usb.h"

static const char *TAG = "app_usb";

/**
 * @brief       USB PHY初始化
 * @param       无
 * @retval      无
 */
static void usb_phy_init(void)
{
    usb_phy_handle_t phy_hdl;
    // Configure USB PHY - ESP32-P4 使用 UTMI PHY
    usb_phy_config_t phy_conf = {
        .controller = USB_PHY_CTRL_OTG,
        .otg_mode = USB_OTG_MODE_DEVICE,
        .target = USB_PHY_TARGET_UTMI,  /* ESP32-P4 必须使用 UTMI PHY */
    };
    usb_new_phy(&phy_conf, &phy_hdl);
}

/**
 * @brief       USB设备任务
 * @param       arg:未使用传参
 * @retval      无
 */
static void tusb_device_task(void *arg)
{
    (void)arg;

    while (1)
    {
        tud_task(); /* tud 任务 */
        vTaskDelay(pdMS_TO_TICKS(1)); /* 让出CPU，避免看门狗超时 */
    }
}

/**
 * @brief       USB初始化
 * @param       无
 * @retval      ESP_OK:初始化成功，其他为初始化失败
 */
esp_err_t app_usb_init(void)
{
    esp_err_t ret = ESP_OK;
    /* USN PHY初始化 */
    usb_phy_init();

    bool usb_init = tusb_init();

    if (!usb_init)
    {
        ESP_LOGE(TAG, "USB Device Stack Init Fail");
        return ESP_FAIL;
    }

    /* Vendor (Windows驱动模式) */
#if CFG_TUD_VENDOR
    ret = app_vendor_init();
    ESP_RETURN_ON_FALSE(ret == ESP_OK, ESP_FAIL, TAG, "app_vendor_init failed");
#endif
    /* HID(触摸) */
#if CFG_TUD_HID
    ret = app_hid_init();
    ESP_RETURN_ON_FALSE(ret == ESP_OK, ESP_FAIL, TAG, "app_hid_init failed");
#endif
    /* USB Audio（音频） */
#if CFG_TUD_AUDIO
    ret =  app_uac_init();
    ESP_RETURN_ON_FALSE(ret == ESP_OK, ESP_FAIL, TAG, "app_uac_init failed");
#endif

    xTaskCreate(tusb_device_task, "tusb_device_task", 4096, NULL, USB_TASK_PRIORITY, NULL);
    return ret;
}

/************************************************** TinyUSB callbacks ***********************************************/
/**
 * @brief       USB设备挂载时调用
 * @param       无
 * @retval      无
 */
void tud_mount_cb(void)
{
    ESP_LOGI(TAG, "USB Mount");
}

/**
 * @brief       USB设备卸载时调用
 * @param       无
 * @retval      无
 */
void tud_umount_cb(void)
{
    ESP_LOGI(TAG, "USB Un-Mount");
}

/**
 * @brief       USB 总线挂载时调用（在7ms内，设备从母线吸取的平均电流必须小于 2.5 mA）
 * @param       remote_wakeup_en:如果主机允许，我们可以远程唤醒
 * @retval      无
 */
void tud_suspend_cb(bool remote_wakeup_en)
{
    (void) remote_wakeup_en;
    ESP_LOGI(TAG, "USB Suspend");
}

/**
 * @brief       USB 总线恢复时调用
 * @param       无
 * @retval      无
 */
void tud_resume_cb(void)
{
    ESP_LOGI(TAG, "USB Resume");
}
