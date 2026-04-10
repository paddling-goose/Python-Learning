"""
气泡绘制模块
支持多行文字，气泡高度自适应
"""
import tkinter as tk


def draw(canvas, text: str, cx: int, y_top: int = 2):
    MAX_WIDTH    = 180   # 气泡最大宽度（像素），超出自动换行
    FONT         = ("微软雅黑", 9, "bold")
    PAD_X        = 12
    PAD_Y        = 8
    LINE_HEIGHT  = 16

    # ── 按最大宽度手动折行 ────────────────────────────
    lines = _wrap_text(text, MAX_WIDTH, char_width=9)

    bw   = min(max(max(len(l) for l in lines) * 9 + PAD_X * 2, 80), MAX_WIDTH + PAD_X * 2)
    bh   = LINE_HEIGHT * len(lines) + PAD_Y * 2

    bx1  = max(4, cx - bw // 2)
    bx2  = bx1 + bw
    by1  = y_top
    by2  = by1 + bh
    mid  = (bx1 + bx2) // 2

    # 外黑框
    canvas.create_rectangle(bx1 - 2, by1 - 2, bx2 + 2, by2 + 2,
                             fill="#1A0A00", outline="")
    # 内白底
    canvas.create_rectangle(bx1, by1, bx2, by2,
                             fill="#FFF5EE", outline="")
    # 小尾巴
    canvas.create_rectangle(mid - 4, by2,     mid + 4, by2 + 6,  fill="#FFF5EE", outline="")
    canvas.create_rectangle(mid - 2, by2 + 6, mid + 2, by2 + 10, fill="#FFF5EE", outline="")

    # ── 逐行绘制文字 ──────────────────────────────────
    for i, line in enumerate(lines):
        ty = by1 + PAD_Y + i * LINE_HEIGHT + LINE_HEIGHT // 2
        canvas.create_text(cx, ty,
                           text=line,
                           fill="#1A0A00",
                           font=FONT,
                           anchor="center")


def _wrap_text(text: str, max_width: int, char_width: int = 9) -> list[str]:
    """按最大宽度折行，支持手动换行符"""
    result = []
    for paragraph in text.split("\n"):
        line = ""
        for char in paragraph:
            if (len(line) + 1) * char_width > max_width:
                result.append(line)
                line = char
            else:
                line += char
        result.append(line)
    return result or [""]