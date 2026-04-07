#!/usr/bin/env python3
"""
窗口位置选择辅助工具
通过点击屏幕获取窗口位置和大小
"""

import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("窗口位置选择辅助工具")
    print("=" * 50)
    print()
    print("方法1: 使用 gnome-screenshot 选择窗口")
    print("       点击窗口后，将显示窗口位置和大小")
    print()
    print("方法2: 手动输入位置")
    print("       如果已知窗口位置，可以直接输入")
    print()

    choice = input("选择方法 (1 或 2): ").strip()

    if choice == '1':
        print("\n请点击要投屏的窗口...")
        try:
            # 使用 gnome-screenshot -w 选择窗口
            result = subprocess.run(
                ['gnome-screenshot', '-w', '-B', '-f', '/tmp/window_crop.png'],
                capture_output=True,
                timeout=60
            )

            if result.returncode == 0 and os.path.exists('/tmp/window_crop.png'):
                from PIL import Image
                img = Image.open('/tmp/window_crop.png')
                w, h = img.size
                print(f"\n窗口截图已保存: /tmp/window_crop.png")
                print(f"窗口大小: {w} x {h}")
                print()
                print("请输入窗口在屏幕上的位置:")
                x = input("X坐标 (默认为窗口左上角，输入0或实际位置): ").strip()
                y = input("Y坐标 (默认为窗口左上角，输入0或实际位置): ").strip()

                x = int(x) if x else 0
                y = int(y) if y else 0

                print()
                print("=" * 50)
                print("裁剪参数:")
                print(f"  --crop {x},{y},{w},{h}")
                print()
                print("投屏命令:")
                print(f"  python3 screen_stream_portal.py -w --crop {x},{y},{w},{h} --no-test")
                print("=" * 50)

                os.unlink('/tmp/window_crop.png')
            else:
                print("窗口截图失败")
        except subprocess.TimeoutExpired:
            print("窗口选择超时")
        except Exception as e:
            print(f"错误: {e}")

    elif choice == '2':
        print("\n请输入窗口位置和大小:")
        x = input("X坐标: ").strip()
        y = input("Y坐标: ").strip()
        w = input("宽度: ").strip()
        h = input("高度: ").strip()

        if x and y and w and h:
            x, y, w, h = int(x), int(y), int(w), int(h)
            print()
            print("=" * 50)
            print("裁剪参数:")
            print(f"  --crop {x},{y},{w},{h}")
            print()
            print("投屏命令:")
            print(f"  python3 screen_stream_portal.py -w --crop {x},{y},{w},{h} --no-test")
            print("=" * 50)
        else:
            print("输入不完整")

    else:
        print("无效选择")


if __name__ == '__main__':
    main()