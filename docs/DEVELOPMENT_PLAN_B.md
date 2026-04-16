# 方案 B：CDP 截图 + USB 显示 开发方案

**更新时间**: 2026-04-14
**目标帧率**: 45 fps (受限于截图速率)
**硬件**: ESP32-P4 + RGB LCD 800×480 + USB HS

---

## 1. 系统架构

```
┌──────────────────────────────────────────────────────────────────┐
│                           PC                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │  AIRI App   │───▶│ CDP Server   │───▶│ USB Bulk OUT     │  │
│  │  (Canvas)   │    │ (截图)        │    │ (EP1)           │  │
│  └──────────────┘    └──────────────┘    └────────┬─────────┘  │
│                                                  │  USB HS     │
└──────────────────────────────────────────────────┼──────────────┘
                                                   │
                                            ┌──────▼──────┐
                                            │  ESP32-P4   │
                                            │  JPEG 硬件   │──▶ LCD 800×480
                                            │  解码        │
                                            └─────────────┘
```

## 2. 瓶颈分析

### 2.1 各环节延迟预算

| 环节 | 当前 | 目标 | 优化空间 |
|------|------|------|----------|
| CDP 截图编码 | ~60ms | ~22ms (45fps) | **主要瓶颈** |
| USB 传输 | ~3ms | ~3ms | 固定开销 |
| JPEG 硬件解码 | ~8ms | ~8ms | 固定开销 |
| LCD 刷新 | ~14ms | ~14ms | 固定开销 |
| **总计** | **~85ms** | **~47ms** | |

### 2.2 截图速率瓶颈根因

CDP `Page.captureScreenshot` 瓶颈：
1. **Chromium 渲染管线** - 必须完成一帧渲染才能截图
2. **软件 JPEG 编码** - libjpeg 编码 800×480 约 20-30ms
3. **进程间通信** - WebSocket 序列化开销

### 2.3 优化方向

| 方向 | 方法 | 预期提升 |
|------|------|----------|
| 并行截图 | 流水线化，边显示边截下一帧 | 2-3× |
| 降低分辨率 | 截取 400×240 放大到 800×480 | 4× 编码提速 |
| 降低 JPEG 质量 | 50-60 质量 | 2× 编码提速 |
| 硬件加速 | 研究 Chromium GPU 加速截图 | 待定 |

---

## 3. 流水线架构设计

### 3.1 理想流水线 (3级)

```
时间 ─────────────────────────────────────────────────────────▶

帧 N:   [截图1]-->[传输1]--> [解码1]--> [显示1]
帧N+1:             [截图2]--> [传输2]--> [解码2]--> [显示2]
帧N+2:                       [截图3]--> [传输3]--> [解码3]--> [显示3]
         ▲                                                   ▲
         └──────────────── 流水线深度 3 ─────────────────────┘
```

**理论帧率 = 1 / max(截图延迟, 传输延迟, 解码延迟)**

### 3.2 各环节并行分析

| 环节 | 耗时 | 是否可并行 |
|------|------|-----------|
| CDP 截图 | ~60ms | **否** - 依赖 Chromium |
| USB 传输 | ~3ms | **可** - 与截图部分重叠 |
| JPEG 解码 | ~8ms | **可** - 与截图部分重叠 |
| LCD 显示 | ~14ms | **可** - 与截图完全并行 |

**实际瓶颈**: CDP 截图 (~60ms) 限制了理论最大帧率 ~16fps

**若要达到 45fps**: 截图必须优化到 ~22ms

---

## 4. 硬件接口定义

### 4.1 ESP32-P4 USB 配置

| 参数 | 值 |
|------|-----|
| VID | 0x303A |
| PID | 0x2986 |
| 速度 | USB 2.0 High Speed |
| 端点 | EP1 OUT (Bulk) |

### 4.2 UDSP 帧协议

```
Offset  Size  Type   Description
------  ----  -----  -----------
00      4     char   magic[4] = "UDSP"
04      2     uint16 type     = 3 (JPEG)
06      2     uint16 width    = 800
08      2     uint16 height   = 480
10      4     uint32 len      = payload 长度
14      4     uint32 frame_id = 帧序号
--      --    --      --
18      len   byte[]  JPEG 数据
```

### 4.3 USB 传输参数

| 参数 | 值 |
|------|-----|
| MTU | 1024 bytes (BULK) |
| 每帧包数 | ~100 (800×480 JPEG@70 ≈ 100KB) |
| 传输间隔 | 微帧级 (125μs) |

---

## 5. 软件设计

### 5.1 PC 端 (Python)

```
airicap/
├── capture/
│   ├── cdp_client.py      # CDP WebSocket 客户端
│   ├── frame_buffer.py    # 环形缓冲区 (3帧深度)
│   └──流水线.py           # 并行执行引擎
├── usb/
│   └── bulk_transfer.py    # USB Bulk 传输
├── main.py                # 入口
└── config.py             # 配置
```

#### 5.1.1 CDP 客户端

```python
# cdp_client.py
import asyncio
import websockets
import json
import struct

class CDPCapture:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.ws = None
        self.frame_id = 0

    async def connect(self):
        self.ws = await websockets.connect(self.ws_url)

    async def capture_jpeg(self) -> bytes:
        """截取一帧 JPEG"""
        # 发送截图请求
        await self.ws.send(json.dumps({
            "id": 1,
            "method": "Page.captureScreenshot",
            "params": {
                "format": "jpeg",
                "quality": 60,  # 降低质量换取速度
                "fromSurface": True
            }
        }))

        # 接收响应
        resp = await self.ws.recv()
        data = json.loads(resp)

        if "result" not in data:
            raise RuntimeError("Screenshot failed")

        # 解码 base64
        import base64
        return base64.b64decode(data["result"]["data"])

    async def close(self):
        if self.ws:
            await self.ws.close()
```

#### 5.1.2 USB 传输

```python
# bulk_transfer.py
import usb.core
import usb.util
import struct

class USBBulkTransfer:
    VID = 0x303A
    PID = 0x2986
    EP_OUT = 1
    MTU = 1024

    def __init__(self):
        self.dev = None

    def open(self):
        self.dev = usb.core.find(idVendor=self.VID, idProduct=self.PID)
        if self.dev is None:
            raise RuntimeError("Device not found")

        # 分离驱动
        try:
            usb.util.claim_interface(self.dev, 0)
        except:
            pass

    def send_frame(self, jpeg_data: bytes, frame_id: int, width=800, height=480):
        """发送一帧到 ESP32"""
        # 构建 UDSP 帧头
        header = struct.pack(
            '<4sHHII',
            b'UDSP',   # magic
            3,         # type = JPEG
            width,
            height,
            len(jpeg_data),
            frame_id
        )

        # 分包发送
        self.dev.write(self.EP_OUT, header)  # 帧头
        for i in range(0, len(jpeg_data), self.MTU):
            chunk = jpeg_data[i:i + self.MTU]
            self.dev.write(self.EP_OUT, chunk)

    def close(self):
        if self.dev:
            usb.util.release_interface(self.dev, 0)
```

#### 5.1.3 流水线执行引擎

```python
# main.py
import asyncio
import threading
from cdp_client import CDPCapture
from bulk_transfer import USBBulkTransfer
from frame_buffer import RingBuffer

class CapturePipeline:
    def __init__(self, cdp_url: str):
        self.cdp = CDPCapture(cdp_url)
        self.usb = USBBulkTransfer()
        self.buffer = RingBuffer(capacity=3)
        self.frame_id = 0
        self.running = False

    async def start(self):
        await self.cdp.connect()
        self.usb.open()
        self.running = True

        # 启动流水线任务
        asyncio.create_task(self.capture_loop())
        asyncio.create_task(self.send_loop())

    async def capture_loop(self):
        """截图循环 - 持续产出帧"""
        while self.running:
            try:
                jpeg = await self.cdp.capture_jpeg()
                self.buffer.push(jpeg)
            except Exception as e:
                print(f"Capture error: {e}")

    async def send_loop(self):
        """发送循环 - 消费缓冲帧"""
        while self.running:
            jpeg = self.buffer.pop()  # 阻塞等待
            if jpeg:
                self.usb.send_frame(jpeg, self.frame_id)
                self.frame_id += 1

    async def stop(self):
        self.running = False
        await self.cdp.close()
        self.usb.close()
```

#### 5.1.4 环形缓冲区

```python
# frame_buffer.py
import queue

class RingBuffer:
    def __init__(self, capacity: int = 3):
        self.capacity = capacity
        self.queue = queue.Queue(maxsize=capacity)

    def push(self, item):
        """放入新帧 (丢弃旧帧如果满)"""
        try:
            self.queue.put_nowait(item)
        except queue.Full:
            # 丢弃最旧的帧
            try:
                self.queue.get_nowait()
                self.queue.put_nowait(item)
            except:
                pass

    def pop(self, timeout=None):
        """取出帧 (等待新帧)"""
        return self.queue.get(timeout=timeout)
```

### 5.2 ESP32 端

```c
// app_vendor.c

// UDSP 帧头解析
typedef __attribute__((packed)) {
    char     magic[4];      // "UDSP"
    uint16_t type;          // 3 = JPEG
    uint16_t width;
    uint16_t height;
    uint32_t len;
    uint32_t frame_id;
} udsp_header_t;

// JPEG 硬件解码显示
void display_jpeg_frame(uint8_t *jpeg_data, size_t len) {
    // 1. 将 JPEG 数据写入 DMA 缓冲区
    // 2. 触发 JPEG 硬件解码
    // 3. 解码完成后自动发送到 LCD
}

// USB EP1 回调
void usb_ep1_out_callback(uint8_t *data, size_t len) {
    udsp_header_t *hdr = (udsp_header_t *)data;

    if (memcmp(hdr->magic, "UDSP", 4) != 0) {
        return;  // 无效帧
    }

    uint8_t *payload = data + sizeof(udsp_header_t);
    size_t payload_len = hdr->len;

    if (hdr->type == 3) {  // JPEG
        display_jpeg_frame(payload, payload_len);
    }
}
```

---

## 6. 性能优化策略

### 6.1 截图优化 (优先级: 高)

| 优化项 | 方法 | 预期提升 |
|--------|------|----------|
| 降低 JPEG 质量 | quality: 90→60 | 2-3× |
| 降低分辨率 | 截取 400×240 放大 | 4× |
| GPU 加速 | 研究 Chrome --enable-gpu-rasterization | 待定 |
| 流水线 | 3帧深度流水线 | 3× |

### 6.2 推荐配置

```python
# 首次实现配置
CONFIG = {
    "jpeg_quality": 60,       # 平衡质量与速度
    "capture_width": 800,     # 原始分辨率
    "capture_height": 480,
    "pipeline_depth": 3,      # 3帧流水线
    "target_fps": 30,         # 目标帧率
}
```

### 6.3 带宽估算

```
每帧大小 = 800 × 480 × 0.4 (60质量 JPEG 压缩比) ≈ 150KB
30fps 带宽 = 150KB × 30 = 4.5MB/s ≈ 36Mbps
USB HS 可用带宽 = 480Mbps (仍有大量余量)
```

---

## 7. 实现步骤

### Phase 1: 基础通信 (1-2天)

- [ ] PC 连接 ESP32 USB
- [ ] 实现 UDSP 协议解析
- [ ] 验证 USB 传输通路
- [ ] ESP32 显示测试图案

### Phase 2: CDP 集成 (1天)

- [ ] 实现 CDP 截图客户端
- [ ] 连接 AIRI 获取截图
- [ ] 验证截图数据流

### Phase 3: 流水线 (2-3天)

- [ ] 实现环形缓冲区
- [ ] 实现 3 帧深度流水线
- [ ] 测量实际帧率

### Phase 4: 优化 (持续)

- [ ] 调整 JPEG 质量参数
- [ ] 尝试降低分辨率
- [ ] 优化 ESP32 解码缓冲

---

## 8. 测试计划

### 8.1 单元测试

| 测试项 | 验证方法 |
|--------|----------|
| CDP 连接 | 能否获取截图 |
| USB 传输 | 能否发送完整帧 |
| UDSP 解析 | ESP32 正确解析帧头 |

### 8.2 性能测试

| 指标 | 测量方法 |
|------|----------|
| 帧率 | 计数器 / 秒 |
| 延迟 | 截帧时间戳 - 显示时间戳 |
| CPU 使用 | top / htop |

### 8.3 验收标准

| 指标 | 目标 | 最低可接受 |
|------|------|-----------|
| 帧率 | 30 fps | 20 fps |
| 延迟 | < 100ms | < 150ms |
| 显示效果 | 流畅无撕裂 | 基本可看 |

---

## 9. 已知问题

| 问题 | 影响 | 解决方案 |
|------|------|----------|
| CDP 截图是瓶颈 | 无法达到 45fps | 流水线 + 降低分辨率 |
| Wayland 透明度 | tkinter 不支持 | 使用 Xorg 或 PipeWire |
| USB 权限 | 普通用户无法访问 | udev 规则 |

---

## 10. 附录

### 10.1 参考资源

- [ESP32-P4 数据手册](/home/nini/airi_esp32p4/usb_800x480_RGBLCD/esp32-p4_datasheet_.md)
- [UDSP 协议定义](/home/nini/airi_esp32p4/usb_800x480_RGBLCD/README airi.md)
- [AIRI CLI 适配器](/home/nini/clis/airi/)

### 10.2 文件索引

```
airicap/
├── src/
│   ├── cdp_client.py      # CDP 截图
│   ├── usb_transfer.py    # USB 传输
│   ├── pipeline.py        # 流水线
│   └── main.py            # 入口
├── esp32/
│   └── app_vendor.c       # ESP32 固件修改
├── config.py
├── requirements.txt
└── README.md
```
