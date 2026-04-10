import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk

# 气泡图片里，文字可用区域（根据你的画稿量一下）
TEXT_AREA_TOP    = 40    # 距图片顶部
TEXT_AREA_BOTTOM = 480   # 距图片顶部（尾巴以上）
TEXT_AREA_LEFT   = 55
TEXT_AREA_RIGHT  = 590

BUBBLE_IMG_SIZE  = 648   # 原图尺寸
BUBBLE_DISPLAY_W = 220   # 显示尺寸，等比缩放
SCALE = BUBBLE_DISPLAY_W / BUBBLE_IMG_SIZE


class Bubble:
    def __init__(self, master: tk.Tk):
        self._master    = master
        self._win       = None
        self._canvas    = None
        self._hide_job  = None
        self._img_tk    = None

        self._font      = tkfont.Font(family="宋体", size=10)
        self._line_h    = 18
        self._scroll_y  = 0
        self._content_h = 0
        self._lines     = []

        # 文字可用区域（缩放后）+ 内边距，避免贴边
        _PAD = 10
        self._tx1 = int(TEXT_AREA_LEFT   * SCALE) + _PAD
        self._tx2 = int(TEXT_AREA_RIGHT  * SCALE) - _PAD
        self._ty1 = int(TEXT_AREA_TOP    * SCALE) + _PAD
        self._ty2 = int(TEXT_AREA_BOTTOM * SCALE) - _PAD
        self._tw  = self._tx2 - self._tx1

        # 显示尺寸
        self._W = BUBBLE_DISPLAY_W
        self._H = int(BUBBLE_IMG_SIZE * SCALE)

        self._load_image()

    def _load_image(self):
        img = Image.open("assets/bubble_00.jpg").convert("RGBA")
        img = img.resize((self._W, self._H), Image.LANCZOS)
        img = self._remove_green_bg(img)

        # tkinter Canvas 不支持透明通道，把 alpha=0 的像素
        # 替换为窗口 transparentcolor（#000001），让系统打孔透明
        bg = Image.new("RGBA", img.size, (0, 0, 1, 255))   # #000001
        img = Image.composite(img, bg, img.split()[3])      # alpha 做蒙版
        self._img_tk = ImageTk.PhotoImage(img.convert("RGB"))

    @staticmethod
    def _remove_green_bg(img: Image.Image, spill_fix: bool = True) -> Image.Image:
        """去除绿幕背景，可选抑制边缘绿色溢出"""
        data = img.getdata()
        new_data = []
        for r, g, b, a in data:
            if g > 80 and g > r * 1.4 and g > b * 1.4:
                new_data.append((0, 0, 0, 0))          # 完全透明
            elif spill_fix and g > r + 20 and g > b + 20:
                corrected_g = (r + b) // 2             # 压低溢出的绿色
                new_data.append((r, corrected_g, b, a))
            else:
                new_data.append((r, g, b, a))
        img.putdata(new_data)
        return img

    # ── 对外接口 ─────────────────────────────────────

    def show(self, text: str, anchor_x: int, anchor_y: int, duration: int = 5000):
        self._cancel_hide()
        self._lines    = self._wrap(text)
        self._scroll_y = 0
        self._content_h = len(self._lines) * self._line_h + 8

        if self._win is None:
            self._build()

        x = anchor_x - self._W // 2
        y = anchor_y - self._H
        self._win.geometry(f"{self._W}x{self._H}+{x}+{y}")
        self._win.deiconify()
        self._redraw()

        if duration > 0:
            self._hide_job = self._master.after(duration, self.hide)

    def hide(self):
        self._cancel_hide()
        if self._win:
            self._win.withdraw()

    # ── 构建 ─────────────────────────────────────────

    def _build(self):
        w = tk.Toplevel(self._master)
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.attributes("-transparentcolor", "#000001")
        w.config(bg="#000001")
        w.withdraw()

        c = tk.Canvas(w, width=self._W, height=self._H,
                      bg="#000001", highlightthickness=0)
        c.pack()

        c.bind("<Enter>",         self._on_enter)
        c.bind("<Leave>",         self._on_leave)
        c.bind("<ButtonPress-1>", self._on_drag_start)
        c.bind("<B1-Motion>",     self._on_drag_move)
        c.bind("<MouseWheel>",    self._on_wheel)

        self._win    = w
        self._canvas = c

    # ── 绘制 ─────────────────────────────────────────

    def _redraw(self):
        c = self._canvas
        c.delete("all")

        # 气泡图片
        c.create_image(0, 0, image=self._img_tk, anchor="nw")

        # 文字区域（裁剪在 ty1~ty2 之间）
        cx     = (self._tx1 + self._tx2) // 2
        clip_h = self._ty2 - self._ty1

        # 内容少时整体垂直居中；内容多时从 ty1 顶部开始（可滚动）
        if self._content_h <= clip_h:
            text_top = self._ty1 + (clip_h - self._content_h) // 2
        else:
            text_top = self._ty1

        cx = (self._tx1 + self._tx2) // 2
        for i, line in enumerate(self._lines):
            ty = text_top + i * self._line_h - self._scroll_y + self._line_h // 2
            if ty < self._ty1 or ty > self._ty2:
                continue
            c.create_text(cx, ty, text=line,
                          fill="#1A0A00", font=self._font, anchor="center")

        # 滚动条（内容超出时显示）
        if self._content_h > clip_h:
            ratio = clip_h / self._content_h
            bar_h = max(int(clip_h * ratio), 16)
            bar_y = self._ty1 + int((self._scroll_y / self._content_h) * clip_h)
            c.create_rectangle(self._tx2 - 4, bar_y,
                               self._tx2 - 1, bar_y + bar_h,
                               fill="#888", outline="")

    # ── 事件 ─────────────────────────────────────────

    def _on_enter(self, _):
        self._cancel_hide()

    def _on_leave(self, _):
        self._hide_job = self._master.after(2000, self.hide)

    def _on_drag_start(self, e):
        self._drag_y = e.y

    def _on_drag_move(self, e):
        dy = self._drag_y - e.y
        self._drag_y = e.y
        self._clamp_scroll(self._scroll_y + dy)
        self._redraw()

    def _on_wheel(self, e):
        self._clamp_scroll(self._scroll_y - e.delta // 2)
        self._redraw()

    def _clamp_scroll(self, val):
        max_s = max(0, self._content_h - (self._ty2 - self._ty1))
        self._scroll_y = max(0, min(val, max_s))

    def _cancel_hide(self):
        if self._hide_job:
            self._master.after_cancel(self._hide_job)
            self._hide_job = None

    # ── 折行 ─────────────────────────────────────────

    def _wrap(self, text: str) -> list[str]:
        result = []
        for para in text.split("\n"):
            line = ""
            for ch in para:
                if self._font.measure(line + ch) > self._tw:
                    if line:
                        result.append(line)
                    line = ch
                else:
                    line += ch
            result.append(line)
        return result or [""]