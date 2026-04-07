#include "tusb.h"
#include "tusb_config.h"
#include "uac_config.h"
#include "usb_descriptors.h"
#include "uac_descriptors.h"
// #include "uvc_descriptors.h"  /* Removed - using TinyUSB macros instead */
#include "lcd.h"

/* 一组接口必须有一个唯一的产品ID，因为PC会在第一次插入设备后保存设备驱动程序
 *
 * 数据包位图:
 *   [MSB]  VIDEO | AUDIO | MIDI | HID | MSC | CDC          [LSB]
 */
#define _PID_MAP(itf, n)  ( (CFG_TUD_##itf) << (n) )
#ifndef USB_PID
#define USB_PID           (0x4000 | _PID_MAP(CDC, 0) | _PID_MAP(MSC, 1) | _PID_MAP(HID, 2) | \
    _PID_MAP(MIDI, 3) | _PID_MAP(AUDIO, 4) | _PID_MAP(VIDEO, 5) | _PID_MAP(VENDOR, 6) )
#endif

/* 设备描述符 */
tusb_desc_device_t const desc_device = {
    .bLength            = sizeof(tusb_desc_device_t),
    .bDescriptorType    = TUSB_DESC_DEVICE,
    .bcdUSB             = 0x0200,

    /* Use Interface Association Descriptor (IAD) for Video */
    /* As required by USB Specs IAD's subclass must be common class (2) and protocol must be IAD (1) */
    .bDeviceClass       = TUSB_CLASS_UNSPECIFIED,
    .bDeviceSubClass    = TUSB_CLASS_UNSPECIFIED,
    .bDeviceProtocol    = TUSB_CLASS_UNSPECIFIED,

    .bMaxPacketSize0    = CFG_TUD_ENDPOINT0_SIZE,

    .idVendor           = USB_VID,
    .idProduct          = USB_PID,
    .bcdDevice          = 0x0101,

    .iManufacturer      = 0x01,
    .iProduct           = 0x02,
    .iSerialNumber      = 0x03,

    .bNumConfigurations = 0x01
};

/**
 * @brief       当收到获取设备描述符时调用
 * @param       无
 * @retval      描述符指针
 */
uint8_t const *tud_descriptor_device_cb(void)
{
    return (uint8_t const *) &desc_device;
}

/* HID报告描述符 - 已禁用触摸功能，使用空报告
uint8_t const desc_hid_report[] = {
    TUD_HID_REPORT_DESC_TOUCH_SCREEN(REPORT_ID_TOUCH, LCD_WIDTH, LCD_HEIGHT),
};
*/
uint8_t const desc_hid_report[] = {
    0x06, 0x00, 0xFF,
    0x09, 0x01,
    0xA1, 0x01,
    0x09, 0x03,
    0x09, 0x04,
    0x15, 0x00,
    0x25, 0xFF,
    0x75, 0x08,
    0x95, 0x01,
    0x81, 0x02,
    0x95, 0x01,
    0x81, 0x01,
    0xC0,
};

/**
 * @brief       HID报告描述符回调函数
 * @param       instance:未使用
 * @retval      HID报告描述符
 */
uint8_t const * tud_hid_descriptor_report_cb(uint8_t instance)
{
    (void) instance;
    return desc_hid_report;
}

/* Vendor 类描述符 */
#if CFG_TUD_VENDOR
#define VENDOR_DESC_TOTAL_LEN  (TUD_VENDOR_DESC_LEN)
#define VENDOR_DESC_CONTENT    TUD_VENDOR_DESCRIPTOR(ITF_NUM_VENDOR, 0, EPNUM_VENDOR_OUT, (0x80 | EPNUM_VENDOR_IN), VENDOR_BUF_SIZE),
#else
#define VENDOR_DESC_TOTAL_LEN  0
#define VENDOR_DESC_CONTENT
#endif

/* 配置描述符 */
#define CONFIG_TOTAL_LEN    (TUD_CONFIG_DESC_LEN + VENDOR_DESC_TOTAL_LEN + \
                             TUD_HID_DESC_LEN * CFG_TUD_HID + \
                             CFG_TUD_AUDIO_FUNC_1_DESC_LEN * CFG_TUD_AUDIO)

uint8_t const desc_fs_configuration[] = {
    /* 配置编号、接口计数、字符串索引、总长度、属性、功率(单位:mA) */
    TUD_CONFIG_DESCRIPTOR(1, ITF_NUM_TOTAL, 0, CONFIG_TOTAL_LEN, 0, 100),
    /* Vendor Class */
    VENDOR_DESC_CONTENT
#if CFG_TUD_HID
    TUD_HID_DESCRIPTOR(ITF_NUM_HID, 5, HID_ITF_PROTOCOL_NONE, sizeof(desc_hid_report), (0x80 | EPNUM_HID_DATA), CFG_TUD_HID_EP_BUFSIZE, 10),
#endif
#if CFG_TUD_AUDIO
    TUD_AUDIO_DESCRIPTOR(ITF_NUM_AUDIO_CONTROL, 6, EPNUM_AUDIO_OUT, (0x80 | EPNUM_AUDIO_IN), (0x80 | EPNUM_AUDIO_FB)),
#endif
};

/**
 * @brief       当接收到获取配置描述符时调用
 * @param       index:未使用
 * @retval      应用程序返回描述符指针
 */
uint8_t const *tud_descriptor_configuration_cb(uint8_t index)
{
    (void) index; /* 对于多种配置 */
    return desc_fs_configuration;
}

/* 字符串描述符 */
char const *string_desc_arr [] = {
    (const char[]) { 0x09, 0x04 },      /* 0: 支持的语言是英语 (0x0409) */
    USB_MANUFACTURER,                   /* 1: 制造商 */
    "DNESP32P4",                        /* 2: 产品 */
    "01-2025",                          /* 3: 序列号，应使用芯片ID */
#if CFG_TUD_AUDIO
    "atk uac",                          /* 6: UAC接口 */
    "speaker",                          /* 7: UAC接口（喇叭） */
    "mic",                              /* 8: UAC接口（咪头） */
#endif
};

static uint16_t _desc_str[32];

/**
 * @brief       收到获取字符串描述符请求时调用
 * @param       index:配置索引
 * @param       langid:未使用
 * @retval      应用程序返回描述符指针，其内容必须存在足够长的时间以完成传输
 */
uint16_t const *tud_descriptor_string_cb(uint8_t index, uint16_t langid)
{
    (void) langid;

    uint8_t chr_count;

    if (index == 0) {
        memcpy(&_desc_str[1], string_desc_arr[0], 2);
        chr_count = 1;
    }
    else
    {
        /* Note: the 0xEE index string is a Microsoft OS 1.0 Descriptors. */
        /* https://docs.microsoft.com/en-us/windows-hardware/drivers/usbcon/microsoft-defined-usb-descriptors */

        if (!(index < sizeof(string_desc_arr) / sizeof(string_desc_arr[0])))
        {
            return NULL;
        }

        const char *str = string_desc_arr[index];

        /* 最大长度 */
        chr_count = (uint8_t) strlen(str);

        if (chr_count > 31)
        {
            chr_count = 31;
        }

        /* 将ASCII字符串转换为UTF-16 */
        for (uint8_t i = 0; i < chr_count; i++)
        {
            _desc_str[1 + i] = str[i];
        }
    }

    /* 首个字节是长度（包括标头），第二个字节是字符串类型 */
    _desc_str[0] = (uint16_t)((TUSB_DESC_STRING << 8) | (2 * chr_count + 2));

    return _desc_str;
}