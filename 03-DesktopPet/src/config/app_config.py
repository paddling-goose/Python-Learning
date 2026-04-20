import os

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _assets(*names):
    """拼接 assets/ 路径，少写重复代码。"""
    return [os.path.join(_ROOT, "assets", n) for n in names]


# 显示
PET_SIZE         = 70
BOUNCE_AMPLITUDE = 4
TRANSPARENT_COLOR = "#010101"

# 动画设置 
FRAME_INTERVAL = 50   # ms，每帧间隔

BLINK_DURATION = 150  # ms，眨眼持续时间
BLINK_MIN      = 2000
BLINK_MAX      = 5000

# 气泡
IDLE_MIN = 25000        # ms，空闲提醒最短间隔
IDLE_MAX = 50000

# 图片
# key 与各状态类的 FRAME_KEY 对应；新增状态只需在此加一行 + 放好图片。
#TODO - drag
ASSETS = {
    "default": _assets("default_00.jpg", "default_01.jpg"),
    "blink":   _assets("blink_00.jpg"),
    "climb":   _assets("climb_00.jpg", "climb_01.jpg", "climb_02.jpg"),
    "sit":     _assets("sit_00.jpg"),
    "dragged": _assets("drag_00.jpg","drag_01.jpg","drag_02.jpg",),
}

# 文案
GREETINGS = [
    "你好呀！🧡",
    "在学RAG吗~",
    "喝水了吗？💧",
    "休息一下吧！",
    "加油！我看好你",
    "今天写代码了吗",
    "摸摸我嘛！",
]

IDLE_MSGS = [
    "喝水了吗？💧",
    "记得休息哦～",
    "加油！🧡",
    "摸摸我嘛~",
    "站起来动一动！",
]