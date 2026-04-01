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
        img = _remove_white_bg(img)
        frames.append(ImageTk.PhotoImage(img))
    return frames


def _remove_white_bg(img, threshold=230):
    """把接近白色的像素变成透明"""
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        if r > threshold and g > threshold and b > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img