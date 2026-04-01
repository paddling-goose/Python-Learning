import tkinter as tk
import math
import random

import bubble
from config.app_config import *
from loader import load_frames
from behaviors.behavior import Behavior, IDLE


class ClaudePet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("小Claude")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.root.config(bg=TRANSPARENT_COLOR)

        self.W = PET_SIZE + 40
        self.H = PET_SIZE + 60
        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H,
                                bg=TRANSPARENT_COLOR, highlightthickness=0)
        self.canvas.pack()

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.x = sw - self.W - 40
        self.y = sh - self.H - 60
        self.root.geometry(f"+{self.x}+{self.y}")

        self.frames_default = load_frames(ASSETS["default"], PET_SIZE)
        self.frames_blink   = load_frames(ASSETS["blink"],   PET_SIZE)

        self.anim_tick   = 0
        self.blinking    = False
        self.bubble_text = ""
        self.bubble_show = False

        # 行为大脑
        self.behavior = Behavior(PET_SIZE)
        self.behavior.set_position(self.x, self.y)

        self.dragging = False
        self.drag_sx  = 0
        self.drag_sy  = 0

        self._bind_events()
        self._blink_loop()
        self._alert_loop()
        self._draw_loop()

    # ── 绘制 ────────────────────────────────────────────
    def _draw_loop(self):
        self.canvas.delete("all")
        self.anim_tick += 1

        if not self.dragging:
            new_x, new_y, state = self.behavior.update()
            self.x = new_x
            self.y = new_y
            self.root.geometry(f"+{self.x}+{self.y}")

        bounce = 0
        if self.behavior.state == IDLE:
            bounce = int(math.sin(self.anim_tick * 0.07) * BOUNCE_AMPLITUDE)

        cx = self.W // 2
        oy = 48 + bounce

        if self.bubble_show and self.bubble_text:
            bubble.draw(self.canvas, self.bubble_text, cx)

        frames = self.frames_blink if (self.blinking and self.frames_blink) \
                 else self.frames_default

        if frames:
            idx = (self.anim_tick // 8) % len(frames)
            self.canvas.create_image(cx - PET_SIZE // 2, oy,
                                     image=frames[idx], anchor="nw")

        self.root.after(FRAME_INTERVAL, self._draw_loop)

    # ── 事件 ────────────────────────────────────────────
    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        self.canvas.bind("<B1-Motion>",       self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Button-3>",        self._on_right_click)

    def _on_press(self, e):
        self.drag_sx = e.x_root - self.x
        self.drag_sy = e.y_root - self.y
        self.dragging = True
        self.show_bubble(self.behavior.greet())

    def _on_drag(self, e):
        if self.dragging:
            self.x = e.x_root - self.drag_sx
            self.y = e.y_root - self.drag_sy
            self.root.geometry(f"+{self.x}+{self.y}")

    def _on_release(self, e):
        self.dragging = False
        self.behavior.set_position(self.x, self.y)

    def _on_right_click(self, e):
        m = tk.Menu(self.root, tearoff=0)
        m.add_command(label="👋 打个招呼",
                      command=lambda: self.show_bubble(self.behavior.greet()))
        m.add_command(label="🪜 去爬窗口",
                      command=self.behavior.go_climb)
        m.add_command(label="🚶 去任务栏",
                      command=self.behavior.go_taskbar)
        m.add_command(label="🏠 待机",
                      command=lambda: self.behavior.set_position(self.x, self.y))
        m.add_separator()
        m.add_command(label="❌ 关闭", command=self.root.destroy)
        m.tk_popup(e.x_root, e.y_root)

    # ── 气泡 ────────────────────────────────────────────
    def show_bubble(self, text, duration=BUBBLE_DURATION):
        self.bubble_text = text
        self.bubble_show = True
        self.root.after(duration, self._hide_bubble)

    def _hide_bubble(self):
        self.bubble_show = False

    # ── 眨眼 ────────────────────────────────────────────
    def _blink_loop(self):
        self.blinking = True
        self.root.after(BLINK_DURATION,
                        lambda: setattr(self, "blinking", False))
        self.root.after(random.randint(BLINK_MIN, BLINK_MAX), self._blink_loop)

    # ── 提醒循环（alert.py 驱动）────────────────────────
    def _alert_loop(self):
        msg = self.behavior.get_alert()
        if msg and not self.bubble_show:
            self.show_bubble(msg, duration=4000)
        self.root.after(60000, self._alert_loop)  # 每分钟检查一次

    def run(self):
        self.root.after(600, lambda: self.show_bubble("嗨！我是小章鱼 🐙"))
        self.root.mainloop()