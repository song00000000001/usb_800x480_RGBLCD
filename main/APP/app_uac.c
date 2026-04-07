/**
 ******************************************************************************
 * @file        app_uac.c
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       USB Audio驱动 (UAC 已启用)
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

#include "app_uac.h"
#include "usb_device_uac.h"
#include "es8388.h"
#include "myi2s.h"
#include "led.h"
#include "xl9555.h"

static const char *TAG = "app_uac";

/* UAC 音频参数 */
#define UAC_SAMPLE_RATE     24000
#define UAC_CHANNEL_NUM     1
#define UAC_BIT_WIDTH       16

/* 10ms interval * 24000Hz * 1ch * 2bytes = 480 bytes */
#define UAC_FRAME_SIZE       (UAC_SPK_INTERVAL_MS * UAC_SAMPLE_RATE / 1000 * UAC_CHANNEL_NUM * 2)

/**
 * @brief       UAC输出回调 (PC -> 设备, 播放)
 * @param       buf:音频数据缓冲区
 * @param       len:数据长度
 * @param       ctx:回调上下文
 * @retval      ESP_OK:成功
 */
static esp_err_t uac_output_cb(uint8_t *buf, size_t len, void *ctx)
{
    (void)ctx;
    if (buf == NULL || len == 0) {
        return ESP_OK;
    }

    /* 通过I2S发送音频数据到ES8388 DAC播放 */
    i2s_tx_write(buf, len);
    return ESP_OK;
}

/**
 * @brief       UAC输入回调 (设备 -> PC, 录音)
 * @param       buf:音频数据缓冲区
 * @param       len:缓冲区长度
 * @param       bytes_read:实际读取的字节数
 * @param       ctx:回调上下文
 * @retval      ESP_OK:成功
 */
static esp_err_t uac_input_cb(uint8_t *buf, size_t len, size_t *bytes_read, void *ctx)
{
    (void)ctx;
    if (buf == NULL || bytes_read == NULL) {
        return ESP_ERR_INVALID_ARG;
    }

    /* 通过I2S从ES8388 ADC读取麦克风数据 */
    *bytes_read = i2s_rx_read(buf, len);
    return ESP_OK;
}

/**
 * @brief       UAC静音回调
 * @param       mute:静音标志
 * @param       ctx:回调上下文
 * @retval      无
 */
static void uac_set_mute_cb(uint32_t mute, void *ctx)
{
    (void)ctx;
    ESP_LOGI(TAG, "Mute: %s", mute ? "ON" : "OFF");
    if (mute) {
        es8388_hpvol_set(0);
    }
}

/**
 * @brief       UAC音量设置回调
 * @param       volume:音量值 (0-100)
 * @param       ctx:回调上下文
 * @retval      无
 */
static void uac_set_volume_cb(uint32_t volume, void *ctx)
{
    (void)ctx;
    ESP_LOGI(TAG, "Volume: %lu", volume);
    /* ES8388 volume range is 0-33, map 0-100 to 0-33 */
    uint8_t es_volume = (volume * 33) / 100;
    es8388_hpvol_set(es_volume);
}

/**
 * @brief       USB Audio初始化
 * @param       无
 * @retval      ESP_OK:初始化成功
 */
esp_err_t app_uac_init(void)
{
    esp_err_t ret;

    ESP_LOGI(TAG, "Initializing UAC audio...");

    /* 1. 初始化ES8388 codec */
    ret = es8388_init();
    if (ret != 0) {
        ESP_LOGE(TAG, "ES8388 init failed");
        return ESP_FAIL;
    }
    ESP_LOGI(TAG, "ES8388 initialized");

    /* 2. 配置ES8388为同时支持录音和播放模式 */
    es8388_adda_cfg(1, 1);       /* 开启DAC和ADC */
    es8388_input_cfg(0);          /* 配置ADC输入通道 */
    es8388_output_cfg(1, 1);      /* 配置DAC输出通道 */
    es8388_mic_gain(8);           /* MIC增益设置为+24dB (最大) */
    es8388_hpvol_set(20);         /* 设置耳机/喇叭音量 */
    es8388_spkvol_set(20);

    /* 3. 配置ES8388 I2S格式为MSB-left-justified，16bit (匹配ESP32 I2S配置) */
    es8388_i2s_cfg(1, 3);  /* 1=MSB-left-justified, 3=16bit */
    vTaskDelay(pdMS_TO_TICKS(10));  /* 延时确保配置生效 */

    /* 4. MYI2S已在main.c中初始化，这里仅重新配置采样率 */
    /* 配置I2S采样率和位宽以匹配UAC参数 */
    /* 注意：i2s_set_samplerate_bits_sample内部会调用i2s_trx_stop()，所以需要重新启动 */
    i2s_set_samplerate_bits_sample(UAC_SAMPLE_RATE, UAC_BIT_WIDTH);

    /* 5. 启动I2S传输 */
    i2s_trx_start();

    /* 6. 发送静音数据(参考34_music，在启动后发送) */
    uint8_t silence_buf[512];
    memset(silence_buf, 0, sizeof(silence_buf));
    i2s_tx_write(silence_buf, sizeof(silence_buf));
    vTaskDelay(pdMS_TO_TICKS(10));

    /* 7. 打开喇叭功放(SPK_EN=0有效，参考34_music) */
    xl9555_pin_write(SPK_EN_IO, 0);

    /* 8. 配置UAC设备回调 */
    uac_device_config_t uac_config = {
        .skip_phy_init = true,        /* USB PHY已在app_usb.c中初始化 */
        .output_cb = uac_output_cb,   /* PC->设备音频回调 */
        .input_cb = uac_input_cb,     /* 设备->PC音频回调 */
        .set_mute_cb = uac_set_mute_cb,
        .set_volume_cb = uac_set_volume_cb,
        .cb_ctx = NULL,
    };

    /* 9. 初始化UAC设备 */
    ret = uac_device_init(&uac_config);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "UAC device init failed: %d", ret);
        return ret;
    }

    ESP_LOGI(TAG, "UAC audio initialized successfully");
    ESP_LOGI(TAG, "  - Sample rate: %d Hz", UAC_SAMPLE_RATE);
    ESP_LOGI(TAG, "  - Channels: %d", UAC_CHANNEL_NUM);
    ESP_LOGI(TAG, "  - Bit width: %d", UAC_BIT_WIDTH);

    /* Debug: Check SPK_EN status */
    int spk_en = xl9555_pin_read(SPK_EN_IO);
    ESP_LOGI(TAG, "SPK_EN status: %d (should be 0 for speaker enabled)", spk_en);

    /* Debug: Read ES8388 I2S format register (should be 0x18 for MSB-left-justified 16bit) */
    uint8_t reg23;
    es8388_read_reg(23, &reg23);
    ESP_LOGI(TAG, "ES8388 Reg23 (I2S format): 0x%02x (should be 0x18)", reg23);

    return ESP_OK;
}