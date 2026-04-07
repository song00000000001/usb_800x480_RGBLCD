#!/usr/bin/env npx ts-node
/**
 * ESP32-P4 USB 屏幕投屏脚本 - TypeScript 版本
 * 使用 x11grab 捕获屏幕并通过 USB 发送
 */

import { findByIds, Device } from 'usb';
import { exec, spawn } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';

// USB 设备参数
const VID = 0x303a;
const PID = 0x2986;

// 屏幕参数
const WIDTH = 800;
const HEIGHT = 480;

// 图像类型
const UDISP_TYPE_JPG = 3;
const JPEG_QUALITY = 70;

// 窗口裁剪区域
let CROP_X = 0;
let CROP_Y = 0;
let CROP_W = 0;
let CROP_H = 0;

// 全局变量
let device: Device | null = null;
let outEndpoint: any = null;
let frameId = 0;
let totalBytes = 0;
let frameCount = 0;
let lastTime = Date.now();

// 命令行参数
interface Args {
  window: boolean;
  noTest: boolean;
  crop: string;
  screenshot: boolean;
  help: boolean;
}

function parseArgs(): Args {
  const args: Args = {
    window: false,
    noTest: false,
    crop: '',
    screenshot: false,
    help: false,
  };

  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case '-w':
      case '--window':
        args.window = true;
        break;
      case '--no-test':
        args.noTest = true;
        break;
      case '--crop':
        args.crop = argv[++i] || '';
        break;
      case '-s':
      case '--screenshot':
        args.screenshot = true;
        break;
      case '-h':
      case '--help':
        args.help = true;
        break;
    }
  }
  return args;
}

function printHelp() {
  console.log(`
ESP32-P4 USB 屏幕投屏脚本 (TypeScript 版本)

用法: npx ts-node screen_stream_portal.ts [选项]

选项:
  -w, --window         窗口选择模式
  --no-test            跳过测试颜色
  --crop <x,y,w,h>     手动指定裁剪区域
  -s, --screenshot     单帧截屏测试
  -h, --help           显示帮助信息
`);
}

interface WindowInfo {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  title: string;
}

async function getWindows(): Promise<WindowInfo[]> {
  const execAsync = promisify(exec);
  const windows: WindowInfo[] = [];

  try {
    const { stdout } = await execAsync('wmctrl -lG', { timeout: 5000 });
    const lines = stdout.trim().split('\n');

    for (const line of lines) {
      if (!line) continue;
      const parts = line.split(/\s+/);
      if (parts.length >= 8) {
        const winId = parts[0];
        const x = parseInt(parts[2]);
        const y = parseInt(parts[3]);
        const w = parseInt(parts[4]);
        const h = parseInt(parts[5]);
        const title = parts.slice(7).join(' ');

        windows.push({ id: winId, x, y, width: w, height: h, title });
      }
    }
  } catch (e) {
    console.log('获取窗口列表失败:', e);
  }

  return windows;
}

async function selectWindowInteractive(): Promise<{ x: number; y: number; width: number; height: number; title: string } | null> {
  const windows = await getWindows();

  if (windows.length === 0) {
    console.log('未找到窗口列表，请在 Portal 对话框中选择窗口');
    return null;
  }

  console.log('\n可用窗口:');
  console.log('-'.repeat(60));

  windows.forEach((w, i) => {
    console.log(`  [${i + 1}] ${w.title}`);
    console.log(`      位置: (${w.x}, ${w.y}) 大小: ${w.width}x${w.height}`);
  });

  console.log('-'.repeat(60));
  console.log('  [0] 在 Portal 对话框中选择（不裁剪）');
  console.log('  [Q] 退出\n');

  return new Promise((resolve) => {
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    readline.question('请选择窗口编号: ', async (choice: string) => {
      readline.close();
      choice = choice.trim().toUpperCase();

      if (choice === 'Q' || choice === '') {
        resolve(null);
        return;
      }

      if (choice === '0') {
        resolve(null);
        return;
      }

      const idx = parseInt(choice) - 1;
      if (idx >= 0 && idx < windows.length) {
        const w = windows[idx];
        console.log(`已选择窗口: ${w.title} (${w.width}x${w.height})`);
        resolve({ x: w.x, y: w.y, width: w.width, height: w.height, title: w.title });
      } else {
        console.log('无效选择');
        resolve(null);
      }
    });
  });
}

/**
 * CRC16 校验
 */
function crc16(data: Buffer): number {
  let crc = 0xffff;
  for (const byte of data) {
    crc ^= byte;
    for (let i = 0; i < 8; i++) {
      if (crc & 1) {
        crc = (crc >> 1) ^ 0xa001;
      } else {
        crc >>= 1;
      }
    }
  }
  return crc;
}

/**
 * 创建帧头 - 包含同步标记
 */
function createFrameHeader(
  width: number,
  height: number,
  payloadSize: number,
  frameType: number,
  frameId: number
): Buffer {
  const SYNC_MARKER = Buffer.from('UDSP');

  const frameIdPayload = (frameId & 0x3ff) | ((payloadSize & 0x3fffff) << 10);

  // 帧类型(1) + 0(1) + 0(2) + 0(2) + width(2) + height(2) + frameIdPayload(4) = 14 bytes
  // 结构: byte0=frame_type, byte1=0, ushort2-3=0, ushort4-5=0, ushort6-7=width, ushort8-9=height, uint10-13=frame_id_payload
  const headerData = Buffer.alloc(14);
  headerData.writeUInt8(frameType, 0);   // byte 0
  headerData.writeUInt16LE(0, 1);        // bytes 1-2
  headerData.writeUInt16LE(0, 3);        // bytes 3-4
  headerData.writeUInt16LE(width, 6);     // bytes 6-7
  headerData.writeUInt16LE(height, 8);    // bytes 8-9
  headerData.writeUInt32LE(frameIdPayload, 10); // bytes 10-13

  const crc = crc16(headerData);
  const crcBuf = Buffer.alloc(2);
  crcBuf.writeUInt16LE(crc, 0);

  // 帧头 = 同步标记(4) + CRC(2) + 数据(14) + 填充到 512 字节
  const fullHeader = Buffer.concat([crcBuf, headerData]);
  const padding = Buffer.alloc(512 - SYNC_MARKER.length - fullHeader.length);
  return Buffer.concat([SYNC_MARKER, fullHeader, padding]);
}

/**
 * 查找并配置 USB 设备
 */
function findUsbDevice(): any {
  console.log(`查找设备 VID=0x${VID.toString(16)}, PID=0x${PID.toString(16)}`);

  device = findByIds(VID, PID) ?? null;
  if (!device) {
    console.log('未找到设备!');
    return null;
  }

  console.log(`找到设备: VID=0x${device.deviceDescriptor.idVendor.toString(16)}, PID=0x${device.deviceDescriptor.idProduct.toString(16)}`);

  try {
    device.open();

    // 使用 Device.interface() 方法获取 Interface 对象
    device.setAutoDetachKernelDriver(true);
    const intf = device.interface(0);

    try {
      if (intf.isKernelDriverActive()) {
        intf.detachKernelDriver();
      }
      intf.claim();
    } catch {
      // 可能已经被分离
    }

    // 获取所有端点 - endpoint() 方法通过 address 获取
    // 或者直接访问 runtime 添加的 endpoints 属性
    const eps = (intf as any).endpoints;
    for (const ep of eps) {
      if (ep.direction === 'out') {
        outEndpoint = ep;
        console.log(`OUT 端点: 0x${ep.address.toString(16)}`);
        break;
      }
    }
  } catch (e) {
    console.log(`配置设备失败: ${e}`);
    return null;
  }

  if (!outEndpoint) {
    console.log('未找到 OUT 端点!');
    return null;
  }

  return outEndpoint;
}

/**
 * 发送一帧图像
 */
async function sendFrame(imageBuffer: Buffer, width: number, height: number): Promise<boolean> {
  if (!outEndpoint) {
    return false;
  }

  const payloadSize = imageBuffer.length;
  const header = createFrameHeader(width, height, payloadSize, UDISP_TYPE_JPG, frameId);

  // 分块发送：header (512) + imageData (每块 512 字节)
  const chunkSize = 512;
  const allData = Buffer.concat([header, imageBuffer]);
  const chunks: Buffer[] = [];
  for (let i = 0; i < allData.length; i += chunkSize) {
    chunks.push(allData.slice(i, Math.min(i + chunkSize, allData.length)));
  }

  // 使用 transferAsync 顺序发送，不打印每个 chunk 的日志
  for (let idx = 0; idx < chunks.length; idx++) {
    try {
      await outEndpoint!.transferAsync(chunks[idx]);
    } catch (err) {
      console.log(`传输错误 chunk ${idx + 1}: ${err}`);
      return false;
    }
  }
  return true;
}

/**
 * 视频流捕获 - 使用 wf-recorder 捕获 wlroots compositor 屏幕
 * 输出 MJPEG 视频流，从中提取 JPEG 帧
 */

// 全局变量：wf-recorder 进程和帧缓冲区
let wfRecorder: any = null;
let wfFrameBuffer = Buffer.alloc(0);
let wfStreaming = false;

/**
 * 启动 wf-recorder 视频流
 */
async function startWfRecorder(): Promise<boolean> {
  if (wfStreaming) return true;

  // 构建裁剪/缩放参数
  let geo = '';
  if (CROP_W > 0 && CROP_H > 0) {
    geo = `-g ${CROP_W}x${CROP_H}+${CROP_X}+${CROP_Y}`;
  }

  // wf-recorder 参数
  // -f mjpeg          MJPEG 编码
  // -c libjpeg        使用 libjpeg 编码器 (ffmpeg 后端)
  // -o <output>       输出到 stdout
  const args = [
    '-f', 'mjpeg',
    '-c', 'libjpeg',
    '-o', '-',  // stdout
  ];

  if (geo) {
    args.push(...geo.split(' '));
  }

  return new Promise((resolve) => {
    wfRecorder = spawn('wf-recorder', args);
    wfStreaming = true;

    wfRecorder.stdout.on('data', (data: Buffer) => {
      wfFrameBuffer = Buffer.concat([wfFrameBuffer, data]);
    });

    wfRecorder.on('close', (code: number) => {
      wfStreaming = false;
      wfRecorder = null;
    });

    wfRecorder.on('error', () => {
      wfStreaming = false;
      wfRecorder = null;
    });

    // 等待一下确保启动成功
    setTimeout(() => resolve(wfStreaming), 100);
  });
}

/**
 * 从 MJPEG 流缓冲区中提取一帧 JPEG
 * JPEG 帧以 FFD8 开始，FF D9 结束
 */
function extractJpegFrame(): Buffer | null {
  const SOI = Buffer.from([0xFF, 0xD8]);  // Start of Image
  const EOI = Buffer.from([0xFF, 0xD9]);  // End of Image

  let startIdx = -1;
  let endIdx = -1;

  // 查找帧开始
  for (let i = 0; i <= wfFrameBuffer.length - 2; i++) {
    if (wfFrameBuffer[i] === 0xFF && wfFrameBuffer[i + 1] === 0xD8) {
      startIdx = i;
      break;
    }
  }

  if (startIdx === -1) return null;

  // 查找帧结束
  for (let i = startIdx + 2; i <= wfFrameBuffer.length - 2; i++) {
    if (wfFrameBuffer[i] === 0xFF && wfFrameBuffer[i + 1] === 0xD9) {
      endIdx = i + 2;
      break;
    }
  }

  if (endIdx === -1) return null;

  // 提取帧
  const frame = wfFrameBuffer.slice(startIdx, endIdx);

  // 保留剩余数据
  wfFrameBuffer = wfFrameBuffer.slice(endIdx);

  return frame;
}

/**
 * 视频流捕获 - 获取一帧
 */
function videoCapture(): Buffer | null {
  if (!wfStreaming) return null;
  return extractJpegFrame();
}

/**
 * 停止 wf-recorder
 */
function stopWfRecorder(): void {
  if (wfRecorder) {
    wfRecorder.kill();
    wfRecorder = null;
    wfStreaming = false;
  }
}

/**
 * 发送测试颜色
 */
async function sendTestColors(): Promise<void> {
  console.log('\n发送测试颜色...');

  const colors = [
    { name: '红', r: 255, g: 0, b: 0 },
    { name: '绿', r: 0, g: 255, b: 0 },
    { name: '蓝', r: 0, g: 0, b: 255 },
  ];

  for (let i = 0; i < colors.length; i++) {
    const { name, r, g, b } = colors[i];

    // 创建测试图像
    const pixels = Buffer.alloc(WIDTH * HEIGHT * 3);
    for (let y = 0; y < HEIGHT; y++) {
      for (let x = 0; x < WIDTH; x++) {
        const offset = (y * WIDTH + x) * 3;
        pixels[offset] = r;
        pixels[offset + 1] = g;
        pixels[offset + 2] = b;
      }
    }

    // 转换为 JPEG
    const jpegBuffer = await encodeToJpeg(pixels, WIDTH, HEIGHT);
    if (jpegBuffer) {
      const ok = await sendFrame(jpegBuffer, WIDTH, HEIGHT);
      if (ok) {
        console.log(`  ${name}: OK`);
      }
    }

    await new Promise((r) => setTimeout(r, 300));
  }
}

/**
 * 简单的 JPEG 编码（使用 ImageMagick）
 */
async function encodeToJpeg(rgbBuffer: Buffer, width: number, height: number): Promise<Buffer | null> {
  // 写入临时 PPM 文件
  const ppmPath = '/tmp/test_frame.ppm';
  const jpegPath = '/tmp/test_frame.jpg';

  // PPM 头 + 数据
  const ppmHeader = Buffer.from(`P6\n${width} ${height}\n255\n`);
  const ppmData = Buffer.concat([ppmHeader, rgbBuffer]);

  await fs.promises.writeFile(ppmPath, ppmData);

  // 使用 ImageMagick 转换，使用 4:2:0 采样因子
  return new Promise((resolve) => {
    exec(`convert -colorspace RGB -type Truecolor -quality ${JPEG_QUALITY} -sampling-factor 4:2:0 ${ppmPath} ${jpegPath}`, async (err) => {
      if (err) {
        resolve(null);
        return;
      }

      try {
        const jpeg = await fs.promises.readFile(jpegPath);
        resolve(jpeg);
      } catch {
        resolve(null);
      }
    });
  });
}

/**
 * 连续捕获并发送屏幕
 */
async function startScreenCapture(): Promise<void> {
  // 启动 wf-recorder 视频流
  const started = await startWfRecorder();
  if (!started) {
    console.log('启动 wf-recorder 失败');
    return;
  }

  console.log('开始屏幕捕获 (wf-recorder MJPEG)...');
  console.log('按 Ctrl+C 停止\n');

  // 注册退出清理
  process.on('SIGINT', () => {
    stopWfRecorder();
    process.exit(0);
  });
  process.on('SIGTERM', () => {
    stopWfRecorder();
    process.exit(0);
  });

  const interval = 16; // ~60fps

  const captureAndSend = async () => {
    try {
      // 从 wf-recorder 流中提取一帧
      const frameBuffer = videoCapture();
      if (!frameBuffer || frameBuffer.length === 0) {
        setTimeout(captureAndSend, interval);
        return;
      }

      const ok = await sendFrame(frameBuffer, WIDTH, HEIGHT);

      if (ok) {
        totalBytes += frameBuffer.length;
        frameCount++;
        frameId++;

        const now = Date.now();
        const elapsed = now - lastTime;

        if (elapsed >= 1000) {
          const fps = (frameCount * 1000) / elapsed;
          const bitrate = (totalBytes * 8) / (elapsed / 1000) / 1000;
          console.log(`FPS: ${fps.toFixed(1)} | 带宽: ${bitrate.toFixed(0)}kbps | 帧: ${frameId}`);
          lastTime = now;
          frameCount = 0;
          totalBytes = 0;
        }
      }
    } catch (e) {
      console.log('捕获错误:', e);
    }

    setTimeout(captureAndSend, interval);
  };

  captureAndSend();
}

/**
 * 单帧截屏测试
 */
async function screenshotTest(): Promise<void> {
  console.log('\n=== 单帧截屏测试 ===');

  // 如果设备已经打开，直接使用现有的 outEndpoint
  if (!outEndpoint) {
    const ep = findUsbDevice();
    if (!ep) {
      return;
    }
  }

  console.log('启动 wf-recorder...');
  const started = await startWfRecorder();
  if (!started) {
    console.log('启动 wf-recorder 失败');
    return;
  }

  // 等待一帧数据
  await new Promise(r => setTimeout(r, 200));

  console.log('捕获屏幕...');
  const frameBuffer = videoCapture();

  // 停止 wf-recorder
  stopWfRecorder();

  if (frameBuffer && frameBuffer.length > 0) {
    console.log(`捕获成功: ${frameBuffer.length} bytes`);
    const ok = await sendFrame(frameBuffer, WIDTH, HEIGHT);

    if (ok) {
      console.log('发送成功!');
    }

    // 保存本地截图
    const screenshotPath = '/tmp/screenshot.jpg';
    await fs.promises.writeFile(screenshotPath, frameBuffer);
    console.log(`本地截图已保存: ${screenshotPath}`);
  } else {
    console.log('捕获失败');
  }
}

/**
 * 主函数
 */
async function main(): Promise<void> {
  const args = parseArgs();

  if (args.help) {
    printHelp();
    return;
  }

  console.log('='.repeat(50));
  console.log('ESP32-P4 无闪白屏幕投屏 (TypeScript 版本)');
  console.log('='.repeat(50));

  // 裁剪设置
  if (args.crop) {
    try {
      const parts = args.crop.split(',').map((p) => parseInt(p.trim()));
      if (parts.length === 4) {
        [CROP_X, CROP_Y, CROP_W, CROP_H] = parts;
        console.log(`裁剪区域: (${CROP_X}, ${CROP_Y}) ${CROP_W}x${CROP_H}`);
      }
    } catch {
      console.log('裁剪区域格式错误: x,y,width,height');
    }
  } else if (args.window) {
    const windowInfo = await selectWindowInteractive();
    if (windowInfo) {
      CROP_X = windowInfo.x;
      CROP_Y = windowInfo.y;
      CROP_W = windowInfo.width;
      CROP_H = windowInfo.height;
      console.log(`将裁剪窗口区域: (${CROP_X}, ${CROP_Y}) ${CROP_W}x${CROP_H}`);
    } else {
      console.log('未选择窗口，将使用完整图像');
    }
  }

  const ep = findUsbDevice();
  if (!ep) {
    return;
  }

  if (!args.noTest) {
    await sendTestColors();
  }

  if (args.screenshot) {
    await screenshotTest();
  } else {
    await startScreenCapture();
  }

  // 保持运行
  process.stdin.resume();
}

// 运行
main().catch(console.error);
