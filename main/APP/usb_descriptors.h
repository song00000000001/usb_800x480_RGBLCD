#ifndef _USB_DESCRIPTORS_H
#define _USB_DESCRIPTORS_H

#include "tusb.h"
#include "app_config.h"

enum {
    REPORT_ID_TOUCH = 1,
    REPORT_ID_COUNT
};

enum {
#if CFG_TUD_VENDOR
    ITF_NUM_VENDOR = 0,
#endif
#if CFG_TUD_HID
    ITF_NUM_HID,
#endif
#if CFG_TUD_AUDIO
    ITF_NUM_AUDIO_CONTROL,
    ITF_NUM_AUDIO_STREAMING_SPK,
    ITF_NUM_AUDIO_STREAMING_MIC,
#endif
    ITF_NUM_TOTAL,
};

enum {
    EPNUM_DEFAULT = 0,
#if CFG_TUD_VENDOR
    EPNUM_VENDOR_OUT,
    EPNUM_VENDOR_IN,
#endif
#if CFG_TUD_HID
    EPNUM_HID_DATA,
#endif
#if CFG_TUD_AUDIO
    EPNUM_AUDIO_OUT,
    EPNUM_AUDIO_IN,
    EPNUM_AUDIO_FB,
#endif
    EPNUM_TOTAL
};

#define TUD_HID_REPORT_DESC_TOUCH_SCREEN(report_id, width, height) \
    HID_USAGE_PAGE   ( HID_USAGE_PAGE_DIGITIZER        ),\
    /* USAGE (Touch Screen) */\
    HID_USAGE        ( 0x04                       ),\
    HID_COLLECTION   ( HID_COLLECTION_APPLICATION ),\
      /* Report ID if any */\
      HID_REPORT_ID ( report_id                 ) \
      /* Input */ \
      /* Finger */ \
      FINGER_USAGE(width, height) \
      FINGER_USAGE(width, height) \
      FINGER_USAGE(width, height) \
      FINGER_USAGE(width, height) \
      FINGER_USAGE(width, height) \
      /* Contact count */\
      HID_USAGE     ( 0x54                                   ),\
      HID_LOGICAL_MAX ( 127                                    ),\
      HID_REPORT_COUNT( 1                                    ),\
      HID_REPORT_SIZE ( 8                                    ),\
      HID_INPUT      ( HID_DATA | HID_VARIABLE | HID_ABSOLUTE ),\
    HID_REPORT_ID ( report_id + 1             ) \
    HID_USAGE (0x55              ),\
    HID_REPORT_COUNT (1               ),\
    HID_LOGICAL_MAX (0x10              ),\
    HID_FEATURE ( HID_DATA | HID_VARIABLE | HID_ABSOLUTE ),\
    HID_COLLECTION_END \

#define FINGER_USAGE(width, height) \
    HID_USAGE     ( 0x42                                   ),\
    HID_COLLECTION  ( HID_COLLECTION_LOGICAL                 ),\
    HID_USAGE     ( 0x42                                   ),\
    HID_LOGICAL_MIN ( 0x00                                 ),\
    HID_LOGICAL_MAX ( 0x01                                 ),\
    HID_REPORT_SIZE ( 1                                    ),\
    HID_REPORT_COUNT( 1                                    ),\
    HID_INPUT      ( HID_DATA | HID_VARIABLE | HID_ABSOLUTE ),\
    HID_REPORT_COUNT( 7                                    ),\
    HID_INPUT      ( HID_CONSTANT | HID_ARRAY | HID_ABSOLUTE ),\
    HID_REPORT_SIZE ( 8                                    ),\
    HID_USAGE     ( 0x51                                   ),\
    HID_REPORT_COUNT( 1                                    ),\
    HID_INPUT      ( HID_DATA | HID_VARIABLE | HID_ABSOLUTE ),\
    HID_USAGE_PAGE ( HID_USAGE_PAGE_DESKTOP                 ),\
    HID_LOGICAL_MAX_N ( width, 2                           ),\
    HID_REPORT_SIZE ( 16                                    ),\
    HID_UNIT_EXPONENT ( 0x0e                                ),\
    /* Inch,EngLinear */\
    HID_UNIT      ( 0x13                                   ),\
    /* X */\
    HID_USAGE     ( 0x30                                   ),\
    HID_PHYSICAL_MIN ( 0                                   ),\
    HID_PHYSICAL_MAX_N ( width, 2                           ),\
    HID_INPUT      ( HID_DATA | HID_VARIABLE | HID_ABSOLUTE ),\
    /* Y */\
    HID_LOGICAL_MAX_N ( height, 2                           ),\
    HID_PHYSICAL_MAX_N ( height, 2                            ),\
    HID_USAGE     ( 0x31                                   ),\
    HID_INPUT      ( HID_DATA | HID_VARIABLE | HID_ABSOLUTE ),\
    HID_USAGE_PAGE ( HID_USAGE_PAGE_DIGITIZER               ),\
    /* Width */\
    HID_USAGE     ( 0x48                                   ),\
    /* Height */\
    HID_USAGE     ( 0x49                                   ),\
    HID_REPORT_COUNT( 2                                    ),\
    HID_INPUT      ( HID_DATA | HID_VARIABLE | HID_ABSOLUTE ),\
    HID_COLLECTION_END, \

#endif
