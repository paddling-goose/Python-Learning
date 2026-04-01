"""
气泡绘制模块
传入 canvas、文字、中心 x 坐标，画出像素风对话气泡
"""


def draw(canvas, text: str, cx: int, y_top: int = 2):
    """
    在 canvas 上绘制对话气泡

    参数：
        canvas  : tkinter Canvas
        text    : 气泡文字
        cx      : 气泡水平中心（像素）
        y_top   : 气泡顶部 y 坐标
    """
    tw   = max(len(text) * 9 + 20, 80)
    bx1  = max(4, cx - tw // 2)
    bx2  = bx1 + tw
    by1  = y_top
    by2  = by1 + 28
    mid  = (bx1 + bx2) // 2

    # 外黑框
    canvas.create_rectangle(bx1 - 2, by1 - 2, bx2 + 2, by2 + 2,
                            fill="#1A0A00", outline="")
    # 内白底
    canvas.create_rectangle(bx1, by1, bx2, by2,
                            fill="#FFF5EE", outline="")
    # 小尾巴
    canvas.create_rectangle(mid - 4, by2, mid + 4, by2 + 6,
                            fill="#FFF5EE", outline="")
    canvas.create_rectangle(mid - 2, by2 + 6, mid + 2, by2 + 10,
                            fill="#FFF5EE", outline="")
    # 文字
    canvas.create_text(cx, (by1 + by2) // 2,
                       text=text, fill="#1A0A00",
                       font=("微软雅黑", 9, "bold"))