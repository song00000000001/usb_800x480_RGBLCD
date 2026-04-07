# AIRI + ESP32-P4 Display Integration

USB streaming of AIRI rendered character images to ESP32-P4 RGB LCD (800x480).

## Overview

| Parameter | Value |
|-----------|-------|
| Display Resolution | 800x480 RGB LCD |
| Target Frame Rate | 15 FPS |
| Primary Platform | Linux |
| USB VID:PID | 0x303A:0x2986 |
| Pixel Format | **BGR565** (firmware LCD expects BGR order) |
| Audio Format | 16-bit 44.1kHz Stereo (future) |

## Architecture

```
AIRI Electron App
    ┌─ Renderer Process
    │   └─ Stage.vue (renders AIRI character)
    │       └─ useUsbDisplayStream composable (frame capture)
    │           └─ UsbDisplayToggle component (UI control)
    │               └─ IPC to Main Process
    └─ Main Process
        └─ usb-display service (USB bulk transfer)
            └─ ESP32-P4 USB Vendor endpoint
                └─ RGB LCD Display (800x480)
                └─ ES8388 Audio Codec (future)
```

## USB Protocol

### Frame Header (512 bytes total)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0-3 | 4 | sync | "UDSP" magic marker |
| 4-5 | 2 | crc16 | MODBUS CRC16 (polynomial 0xA001) |
| 6 | 1 | type | 0=RGB565, 1=RGB888, 2=YUV420, 3=JPEG |
| 7 | 1 | cmd | Command (0) |
| 8-9 | 2 | x | X offset (0) |
| 10-11 | 2 | y | Y offset (0) |
| 12-13 | 2 | width | Frame width |
| 14-15 | 2 | height | Frame height |
| 16-19 | 4 | frame_info | frame_id(10 bits) \| (payload_total(22 bits) << 10) |

### CRC16 Implementation (MODBUS)

```typescript
function crc16Modbus(data: Uint8Array): number {
  let crc = 0xFFFF
  for (const byte of data) {
    crc ^= byte
    for (let j = 0; j < 8; j++) {
      if (crc & 1) crc = (crc >> 1) ^ 0xA001
      else crc >>= 1
    }
  }
  return crc
}
```

**Important:** CRC is calculated over bytes 6-19 (14 bytes of header data after sync+CRC).

### Data Type Values

| Type | Value | Description |
|------|-------|-------------|
| RGB565 | 0 | 16-bit BGR (5-6-5) |
| RGB888 | 1 | 24-bit RGB |
| YUV420 | 2 | YUV format |
| JPEG | 3 | Compressed JPEG (recommended) |

### Firmware Frame Header Definition

Located in `main/APP/app_config.h`:

```c
#define UDISP_SYNC_MARKER           "UDSP"  /* 4-byte sync marker */
#define UDISP_SYNC_MARKER_LEN       4

typedef struct {
    uint8_t  sync[4];               /* "UDSP" sync marker */
    uint16_t crc16;                 /* MODBUS CRC16 */
    uint8_t  type;                  /* Data type: RGB565/RGB888/YUV420/JPG */
    uint8_t  cmd;                   /* Command */
    uint16_t x;                     /* X offset */
    uint16_t y;                     /* Y offset */
    uint16_t width;                 /* Frame width */
    uint16_t height;                /* Frame height */
    uint32_t frame_id: 10;          /* Frame ID (10 bits) */
    uint32_t payload_total: 22;     /* Total payload size (22 bits) */
} __attribute__((packed)) udisp_frame_header_t;
```

**Important Notes:**
- CRC16 is calculated over bytes 6-19 (14 bytes after sync+CRC fields)
- The firmware validates `width == LCD_WIDTH (800)` and `height == LCD_HEIGHT (480)`
- Dimension mismatch frames are dropped with debug logging

### Pixel Format: BGR565

**Critical:** The ESP32-P4 firmware's LCD driver expects **BGR565** format, not RGB565.

When sending raw RGB565 frames, R and B components must be swapped:

```typescript
const b5 = (color.b >> 3) & 0x1F
const g6 = (color.g >> 2) & 0x3F
const r5 = (color.r >> 3) & 0x1F
const bgr565 = (b5 << 11) | (g6 << 5) | r5
```

## Files

### Composables (Renderer Process)

| File | Purpose |
|------|---------|
| `packages/stage-ui/src/composables/frame-capture.ts` | WebGL canvas frame capture with BGR565 support |
| `packages/stage-ui/src/composables/use-usb-display-stream.ts` | AIRI video stream composable |
| `apps/stage-tamagotchi/src/renderer/composables/use-usb-display.ts` | Renderer IPC wrapper for USB display |

### Components

| File | Purpose |
|------|---------|
| `apps/stage-tamagotchi/src/renderer/components/UsbDisplayToggle.vue` | USB display UI toggle component |

### Main Process Services

| File | Purpose |
|------|---------|
| `apps/stage-tamagotchi/src/main/services/usb-display/index.ts` | USB display service with protocol implementation |
| `apps/stage-tamagotchi/src/main/index.ts` | IPC handlers registration |

### Test Scripts

| File | Purpose |
|------|---------|
| `apps/stage-tamagotchi/scripts/test-usb-display.ts` | RGB565 test script (BGR565 format) |
| `apps/stage-tamagotchi/scripts/send_usb_frame.py` | Python USB sender (working reference) |

## Implementation Details

### Main Process IPC Handlers

Registered in `src/main/index.ts`:

```typescript
// USB Display IPC handlers
ipcMain.handle('usb-display:connect', async () => {
  return await usbDisplayService.connect()
})

ipcMain.handle('usb-display:disconnect', async () => {
  await usbDisplayService.disconnect()
})

ipcMain.handle('usb-display:state', () => {
  return usbDisplayService.getState()
})

ipcMain.handle('usb-display:update-config', (_, config) => {
  usbDisplayService.updateConfig(config)
})

ipcMain.on('usb-display:send-frame', async (_, frame) => {
  const { data, format } = frame
  const uint8Array = new Uint8Array(data)
  await usbDisplayService.sendFrame(uint8Array, format)
})
```

### Renderer Process Usage

```typescript
// use-usb-display.ts - IPC wrapper
import { useUsbDisplay } from '@/composables/use-usb-display'

const { isConnected, isStreaming, connect, disconnect, sendFrame } = useUsbDisplay()

// Connect to USB device
await connect()

// Send frame data
await sendFrame(frameData, 'jpeg')
```

### WebGL Frame Capture

For WebGL-rendered content (VRM), use `useUsbDisplayStream`:

```typescript
// use-usb-display-stream.ts
import { useUsbDisplayStream } from '@proj-airi/stage-ui'

const { startStreaming, stopStreaming, isStreaming, framesPerSecond } = useUsbDisplayStream(
  () => canvasElement,
  { width: 800, height: 480, frameRate: 15, format: 'jpeg' }
)

// Start streaming with callback
startStreaming((frame) => {
  // Send frame via IPC
  window.electron.ipcRenderer.invoke('usb-display:send-frame', {
    data: Array.from(frame.data),
    format: frame.format,
  })
})
```

### UI Component

`UsbDisplayToggle.vue` provides a simple UI for:
- Connect/disconnect USB device
- Start/stop frame streaming
- Display current FPS

```vue
<template>
  <UsbDisplayToggle :canvas-element="() => stageRef?.canvasElement()" />
</template>
```

## Test Scripts

### RGB565 Test Frames

```bash
# Send RGB565 test frames (BGR565 format)
npx tsx apps/stage-tamagotchi/scripts/test-usb-display.ts --test-frame --vid=0x303a --pid=0x2986
```

Expected results:
- Red screen (10x10, 100x100, 800x480)
- Green screen
- Blue screen

### Python Reference Sender

```bash
# Send JPEG frame
python3 apps/stage-tamagotchi/scripts/send_usb_frame.py 0x303a 0x2986 800 480 0 "255,0,0" jpeg

# Send RGB565 frame (BGR565)
python3 apps/stage-tamagotchi/scripts/send_usb_frame.py 0x303a 0x2986 800 480 0 "0,0,255"
```

## Debugging

### Common Issues

1. **LIBUSB_ERROR_ACCESS**: Create udev rule:
   ```
   # /etc/udev/rules.d/99-esp32-p4-display.rules
   SUBSYSTEM=="usb", ATTR{idVendor}=="303a", ATTR{idProduct}=="2986", MODE="0666"
   ```

2. **Wrong colors**: Check pixel format is **BGR565**

3. **Device not found**: Check VID/PID matches firmware configuration (0x303A:0x2986)

### Firmware Debug Output

Expected serial output during normal operation:

```
I (856) app_usb: USB Mount
I (860) app_usb: USB Device Stack Init Success
I (900) app_lcd: JPEG buffer allocated: 0x70000000, size=768000
I (950) transfer_task: Input fps: 15.32
I (1000) app_lcd: Display fps: 15.28
```

Debug output for frame reception:

```c
// In tud_vendor_rx_cb
D (1234) app_vendor: USB callback: read 4096 bytes, offset=0, total=4096, receiving=0
D (1235) app_vendor: RX: sync found at 0, type=3, width=800, height=480, payload=384000
D (1236) app_vendor: RX: 50% (192000/384000 bytes)
D (1237) app_vendor: RX: 100% (384000/384000 bytes)
```

Dimension mismatch debug:

```c
D (2345) app_vendor: RX: sync found at 0, type=3, width=640, height=480, payload=307200
D (2346) app_vendor: RX: dimension mismatch, dropping
D (2347) app_vendor: RX: dropped full frame, skipped 307712 bytes total
```

## Current Status

### Firmware Side (ESP32-P4)
- [x] USB Device Stack with TinyUSB
- [x] Vendor mode data reception with protocol parsing
- [x] CRC16 validation (MODBUS 0xA001)
- [x] Frame synchronization with "UDSP" marker
- [x] JPEG decoding with hardware accelerator
- [x] RGB LCD display output (800x480)
- [x] Frame buffer management (8 buffers)
- [x] UAC audio playback/recording (24kHz, 16-bit mono)
- [ ] HID touch reporting (disabled)
- [ ] UVC video mode (Linux V4L2 driver)

### PC Side (AIRI Electron App)
- [x] Frame capture composable with BGR565 support
- [x] USB streaming service with correct protocol
- [x] Test scripts working (verified with ESP32-P4 display)
- [x] AIRI video stream integration composable
- [x] Main process IPC handlers
- [x] Renderer process composable wrapper
- [x] USB display toggle UI component
- [x] Full AIRI character streaming integration (WebGL canvas capture)
- [ ] Audio integration pending

## Integration Checklist

To enable USB display in AIRI:

1. [x] **Add component to UI** - `UsbDisplayToggle` placed in main window (`apps/stage-tamagotchi/src/renderer/pages/index.vue`)
2. [x] **Connect to canvas** - Pass `canvasElement` function from `WidgetStage` component
3. [x] **Test with test script** - Verify USB communication before testing AIRI stream
4. [x] **Optimize frame rate** - Adjust FPS based on USB bandwidth (15 FPS default)

## Firmware Architecture

### Main Task Flow

```
app_main()
    ├── nvs_flash_init()          # NVS初始化
    ├── led_init()                 # LED初始化
    ├── myiic_init()               # I2C总线初始化
    ├── es8388_init()              # ES8388音频Codec初始化
    ├── myi2s_init()               # I2S接口初始化
    ├── xl9555_init()             # XL9555 IO扩展初始化
    ├── app_usb_init()             # USB设备栈初始化
    │   ├── usb_phy_init()        # USB PHY初始化
    │   ├── tusb_init()           # TinyUSB初始化
    │   ├── app_vendor_init()     # Vendor模式初始化
    │   ├── app_hid_init()        # HID初始化（已禁用）
    │   ├── app_uac_init()        # UAC音频初始化
    │   └── xTaskCreate(tusb_device_task)
    └── app_lcd_init()            # LCD初始化和JPEG解码器
```

### Vendor Data Reception Flow

```
tud_vendor_rx_cb()
    ├── tud_vendor_n_available()  # 检查接收数据
    ├── tud_vendor_n_read()       # 读取数据
    ├── Search "UDSP" sync marker
    ├── Validate CRC16
    ├── Parse frame header (512 bytes)
    │   └── udisp_frame_header_t
    ├── Check dimension match (800x480)
    └── buffer_fill()
        └── frame_add_data()
        └── frame_send_filled()   # 发送到显示队列

transfer_task()
    ├── frame_get_filled()        # 等待完整帧
    └── app_lcd_draw()            # 显示帧
        └── jpeg_decoder_process() # JPEG解码（如需要）
        └── esp_lcd_panel_draw_bitmap()
```

### Frame Buffer Management

```
frame_allocate(8, JPEG_BUFFER_SIZE)
    ├── xQueueCreate(empty_fb_queue, 8)
    ├── xQueueCreate(filled_fb_queue, 8)
    └── 8x frame_t allocated

frame_get_empty() → frame_add_data() → frame_send_filled() → frame_get_filled() → frame_return_empty()
```

## Firmware Configuration

### USB Configuration (`app_config.h`)

```c
#define LCD_WIDTH    800
#define LCD_HEIGHT   480

#define TUSB_VID     0x303A
#define TUSB_PID     0x2986

#define JPEG_BUFFER_SIZE   (LCD_WIDTH * LCD_HEIGHT * 2)  // 768000 bytes
#define USB_VENDOR_RX_BUFSIZE  4096
#define USB_FRAME_HEADER_SIZE   512

#define UAC_SAMPLE_RATE    24000
#define UAC_CHANNEL_NUM    1
#define UAC_BIT_WIDTH      16
```

### TinyUSB Configuration (`tusb_config.h`)

```c
// USB High Speed enabled
#define CONFIG_TINYUSB_RHPORT_HS    1

// Vendor class enabled
#define CFG_TUD_VENDOR               1
#define CFG_TUD_VENDOR_RX_BUFSIZE   (512 * 10)  // 5120 bytes

// HID class enabled (but touch reporting disabled in app_hid.c)
#define CFG_TUD_HID                  1

// UAC class enabled
#define CFG_TUD_AUDIO                1
```

### LCD Configuration

- **Resolution**: 800x480
- **Pixel Clock**: 30MHz
- **Format**: RGB565
- **Panel ID**: 0x4384 (from GPIO reading)
- **Buffers**: Single frame buffer (DRAM_ATTR)

## Debugging

### Firmware Debug Output

Enable debug logging in `app_vendor.c`:

```c
ESP_LOGD(TAG, "USB callback: read %d bytes, offset=%d", read_res, offset);
ESP_LOGD(TAG, "RX: sync found at %d, type=%d, width=%d, height=%d", 
         sync_pos, pblt->type, pblt->width, pblt->height);
ESP_LOGD(TAG, "RX: first 20 bytes: %02x %02x ...", ...);
```

### Input FPS Monitoring

Firmware prints input FPS every 100 frames:

```c
// In app_vendor.c transfer_task
if (fps_count == 100) {
    ESP_LOGI(TAG, "Input fps: %.2f", 1000000.0 / ((end_time - start_time) / 100.0));
}
```

### Output FPS Monitoring

Firmware prints display FPS every 100 frames:

```c
// In app_lcd.c app_lcd_draw
if (fps_count == 100) {
    ESP_LOGI(TAG, "Display fps: %.1f", 1000000.0 / ((end_time - start_time) / 100.0));
}
```

### Common Issues

1. **LIBUSB_ERROR_ACCESS**: Create udev rule:
   ```
   # /etc/udev/rules.d/99-esp32-p4-display.rules
   SUBSYSTEM=="usb", ATTR{idVendor}=="303a", ATTR{idProduct}=="2986", MODE="0666"
   ```

2. **Wrong colors**: Check pixel format is **BGR565**

3. **Device not found**: Check VID/PID matches firmware (0x303A:0x2986)

4. **Frame not displaying**: Check dimension match - firmware expects 800x480 exactly

5. **JPEG decode failed**: Check `esp_cache_msync()` is called after decoder output

## Known Issues

- JPEG decoding on firmware outputs BGR565, requiring BGR565 format for raw frames
- Small frames (e.g., 10x10) may not display correctly due to firmware dimension validation
- WebGL canvas capture requires `preserveDrawingBuffer: true` in WebGL context
- HID touch reporting is disabled in firmware (app_hid.c has empty callback)
- UVC mode is commented out in tusb_config.h (CFG_TUD_VIDEO)

## Future Enhancements

1. **Touch Integration**: Enable GT9xxx touch driver and HID touch reporting
2. **UVC Mode**: Implement UVC video class for Linux V4L2免驱 support
3. **Multi-panel Support**: Expand beyond 800x480 to 1024x600 and other resolutions
4. **Audio Improvements**: Stereo support, higher sample rates (44.1kHz/48kHz)
5. **Performance Optimization**: Higher frame rates, lower latency
