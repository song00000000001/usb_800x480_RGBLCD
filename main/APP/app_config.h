/**
 ******************************************************************************
 * @file        app_config.c
 * @author      正点原子团队(ALIENTEK)
 * @version     V1.0
 * @date        2025-01-01
 * @brief       管理配置
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

#ifndef __APP_CONFIG_H
#define __APP_CONFIG_H

#include "stddef.h"
#include "stdint.h"

/*----------------根据屏幕分辨率设置分辨率---------------- */
#define LCD_WIDTH    800
#define LCD_HEIGHT   480

/*----------------USB设备配置---------------- */
/* USB HS使能配置 - 启用 High Speed（USB 3.0 集线器支持） */
#define CONFIG_TINYUSB_RHPORT_HS    1
/* USB设备参数配置 */
#define USB_TASK_PRIORITY           5
#define VENDOR_TASK_PRIORITY        10
#define HID_TASK_PRIORITY           5
/* 设备的 TUSB_VID TUSB_PID 必须符合驱动文件 INF 中 `DeviceName` 的描述 */
#define TUSB_VID                    0x303A
#define TUSB_PID                    0x2986
#define TUSB_MANUFACTURER           "ALIENTEK"          /* 制造商 */
#define TUSB_PRODUCT                "DNESP32-P4 Board"  /* 产品 */

/*----------------USB Audio配置---------------- */
#define UAC_SPEAK_CHANNEL_NUM       1       /* SPEAKER */
#define UAC_MIC_CHANNEL_NUM         1       /* MIC */
#define UAC_DEFAULT_SAMPLE_RATE     24000   /* SAMPLE RATE */
#define UAC_SPK_INTERVAL_MS         10      /* READ INTERVAL in ms */
#define UAC_MIC_INTERVAL_MS         10      /* WRITE INTERVAL in ms */

#define UAC_MIC_TASK_PRIORITY       5       /* MIC任务优先级 */
#define UAC_MIC_TASK_CORE           -1
#define UAC_SPK_NEW_PLAY_INTERVAL   100     /* 喇叭音量 */
#define UAC_SPK_TASK_PRIORITY       5       /* 喇叭任务优先级 */
#define UAC_SPK_TASK_CORE           -1

/*----------------JPEG配置---------------- */
/* JPEG缓存大小 - 足够容纳一帧RGB565 (800*480*2=768000) */
#define JPEG_BUFFER_SIZE            (LCD_WIDTH * LCD_HEIGHT * 2)
/* 接收buf大小 - 增加以提高USB Bulk传输效率
 * ESP32-P4 USB HS Bulk最大包512字节, 更大的缓冲减少中断频率
 * 建议值为16KB~64KB, 需与tusb_config.h中CFG_TUD_VENDOR_RX_BUFSIZE匹配 */
#define USB_VENDOR_RX_BUFSIZE       (16 * 1024)
/* USB帧头实际大小 - Python端填充到512字节 */
#define USB_FRAME_HEADER_SIZE       512

/*----------------帧同步标记---------------- */
#define UDISP_SYNC_MARKER           "UDSP"  /* 4字节同步标记 */
#define UDISP_SYNC_MARKER_LEN       4

/*----------------颜色类型---------------- */
#define UDISP_TYPE_RGB565           0        /* RGB565 */
#define UDISP_TYPE_RGB888           1        /* RGB888 */
#define UDISP_TYPE_YUV420           2        /* YUV420 */
#define UDISP_TYPE_JPG              3        /* JPEG */

typedef struct {
    uint8_t  sync[4];               /* 同步标记 "UDSP" */
    uint16_t crc16;                 /* 循环冗余校验16 */
    uint8_t  type;                  /* 类型 */
    uint8_t  cmd;                    /* 命令 */
    uint16_t x;                     /* x偏移坐标 */
    uint16_t y;                     /* y偏移坐标 */
    uint16_t width;                 /* 宽度 */
    uint16_t height;                /* 高度 */
    uint32_t frame_id: 10;          /* 帧的ID */
    uint32_t payload_total: 22;     /* 32位对齐 */
} __attribute__((packed)) udisp_frame_header_t; /* 描述包的首部结构体 */

/* 描述图像帧的信息结构体 */
typedef struct {
    uint16_t width;                 /* 宽度 */
    uint16_t height;                /* 高速 */
    uint32_t received;              /* 接收大小 */
    uint32_t total;                 /* 总大小 */
} frame_info_t;
/* 图像帧结构体 */
typedef struct {
    size_t data_buffer_len;     /* 帧缓存区最大支持数据长度 */
    size_t data_len;            /* 当前存储帧的数据长度 */
    uint8_t *data;              /* 帧的数据 */
    uint8_t type;               /* 数据类型：UDISP_TYPE_RGB565/RGB888/YUV420/JPG */
    frame_info_t info;          /* 描述一帧的图像成员 */
} frame_t;

/* HID 信息结构体 - 已禁用触摸功能，仅保留结构体定义 */
typedef struct {
    uint32_t report_id;
    uint8_t reserved[32];
} __attribute__((packed)) hid_report_t;

#endif
