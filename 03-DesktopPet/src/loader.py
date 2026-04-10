from PIL import Image, ImageTk
import os


def load_frames(path_list, size):
    frames = []
    for path in path_list:
        if not os.path.exists(path):
            print(f"[警告] 找不到图片: {path}")
            continue
        img = Image.open(path).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        img = _remove_green_bg(img)
        frames.append(ImageTk.PhotoImage(img))
    return frames


def _remove_green_bg(img, spill_fix=True):
    """
    把绿幕背景像素变成透明。
    判断条件：g 明显大于 r 和 b，且 g 本身足够亮。
    spill_fix=True 时同时抑制边缘绿色溢出（green spill）。
    """
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        # 核心绿幕判断
        if g > 80 and g > r * 1.4 and g > b * 1.4:
            # 完全透明
            new_data.append((0, 0, 0, 0))
        elif spill_fix and g > r + 20 and g > b + 20:
            # 边缘溢出：压低 g 通道，保留透明度
            corrected_g = (r + b) // 2
            new_data.append((r, corrected_g, b, a))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img