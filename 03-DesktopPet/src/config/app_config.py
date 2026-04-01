import os

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 图片尺寸
PET_SIZE = 70

# 弹跳幅度（像素）
BOUNCE_AMPLITUDE = 4

# 透明背景色（不要改）
TRANSPARENT_COLOR = "#010101"

# 图片路径
ASSETS = {
    "default": [
        os.path.join(_ROOT, "assets/default_00.jpg"),
        os.path.join(_ROOT, "assets/default_01.jpg"),
    ],
    "blink": [
        os.path.join(_ROOT, "assets/blink_00.jpg"),
    ],
}

# 动画刷新间隔（毫秒）
FRAME_INTERVAL = 50

# 眨眼配置（毫秒）
BLINK_DURATION = 150
BLINK_MIN      = 2000
BLINK_MAX      = 5000

# 空闲提醒间隔（毫秒）
IDLE_MIN = 25000
IDLE_MAX = 50000

# 气泡默认显示时长（毫秒）
BUBBLE_DURATION = 2500

# 点击时随机说的话
GREETINGS = [
    "你好呀！🧡",
    "在学RAG吗~",
    "喝水了吗？💧",
    "休息一下吧！",
    "加油！我看好你",
    "今天写代码了吗",
    "摸摸我嘛！",
]

# 空闲时说的话
IDLE_MSGS = [
    "喝水了吗？💧",
    "记得休息哦～",
    "加油！🧡",
    "摸摸我嘛~",
    "站起来动一动！",
]
