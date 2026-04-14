"""
behaviors/states.py
状态常量 + 速度配置，统一在此定义，各状态文件从这里导入。
"""

# ── 状态名 ─────────────────────────────────────────────────────────────── #
IDLE            = "idle"
WALK_TO_WINDOW  = "walk_to_window"
CLIMB           = "climb"
SIT_ON_WINDOW   = "sit_on_window"
WALK_ON_TASKBAR = "walk_on_taskbar"
FALL            = "fall"

# ── 速度（单位：像素/帧）──────────────────────────────────────────────── #
WALK_SPEED  = 3
CLIMB_SPEED = 2
FALL_SPEED  = 6

# —— 状态对应的图片 ——————————————————————————————————————————————————————#
class ClimbState:
    FRAME_KEY = "climb"   # 对应 ASSETS["climb"]

class SitOnWindowState:
    FRAME_KEY = "sit"

class IdleState:
    FRAME_KEY = "default"  # walk / fall / taskbar 也用 default