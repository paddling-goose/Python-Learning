"""
base.py
状态常量 + 移动基础逻辑
负责：走路、爬墙、坐窗口、任务栏行走、掉落
"""
import random
from api.windows_api import get_target_window, get_taskbar_rect, get_screen_size

# ── 状态常量 ──────────────────────────────────────────
IDLE            = "idle"
WALK_TO_WINDOW  = "walk_to_window"
CLIMB           = "climb"
SIT_ON_WINDOW   = "sit_on_window"
WALK_ON_TASKBAR = "walk_on_taskbar"
FALL            = "fall"

# ── 速度配置 ──────────────────────────────────────────
WALK_SPEED  = 3
CLIMB_SPEED = 2
FALL_SPEED  = 6


class BaseMovement:
    """
    处理桌宠的物理移动和状态切换
    pet.py 通过 behavior.py 间接使用
    """

    def __init__(self, pet_size):
        self.pet_size   = pet_size
        self.state      = IDLE
        self.x          = 100
        self.y          = 100
        self.facing     = 1       # 1=右, -1=左

        self._idle_timer    = 0
        self._target_window = None
        self._climb_side    = "left"

    # ── 每帧更新，返回 (x, y, state) ─────────────────
    def update(self):
        if   self.state == IDLE:            self._update_idle()
        elif self.state == WALK_TO_WINDOW:  self._update_walk_to_window()
        elif self.state == CLIMB:           self._update_climb()
        elif self.state == SIT_ON_WINDOW:   self._update_sit_on_window()
        elif self.state == WALK_ON_TASKBAR: self._update_walk_on_taskbar()
        elif self.state == FALL:            self._update_fall()
        return self.x, self.y, self.state

    def set_position(self, x, y):
        """拖动后同步位置，重置为待机"""
        self.x = x
        self.y = y
        self.state = IDLE
        self._idle_timer = 0

    def go_to(self, state):
        """外部触发状态切换"""
        self.state = state

    # ── IDLE ─────────────────────────────────────────
    def _update_idle(self):
        self._idle_timer += 1
        if self._idle_timer > random.randint(180, 360):
            self._idle_timer = 0
            next_state = random.choices(
                [WALK_TO_WINDOW, WALK_ON_TASKBAR],
                weights=[70, 30]
            )[0]
            self.state = next_state

    # ── WALK_TO_WINDOW ────────────────────────────────
    def _update_walk_to_window(self):
        win = get_target_window()
        if win is None:
            self.state = IDLE
            return

        _, wl, wt, wr, wb = win
        self._target_window = win

        dist_left  = abs(self.x - wl)
        dist_right = abs(self.x - wr)
        self._climb_side = "left" if dist_left < dist_right else "right"
        target_x = wl if self._climb_side == "left" else wr - self.pet_size

        dx = target_x - self.x
        if abs(dx) < WALK_SPEED:
            self.x = target_x
            self.state = CLIMB
        else:
            self.facing = 1 if dx > 0 else -1
            self.x += self.facing * WALK_SPEED

        self.y = self._ground_y()

    # ── CLIMB ─────────────────────────────────────────
    def _update_climb(self):
        win = get_target_window()
        if win is None:
            self.state = FALL
            return

        _, wl, wt, wr, wb = win
        target_y = wt - self.pet_size

        if self.y - target_y < CLIMB_SPEED:
            self.y = target_y
            self._target_window = win
            self.state = SIT_ON_WINDOW
        else:
            self.y -= CLIMB_SPEED

        self.x = wl if self._climb_side == "left" else wr - self.pet_size

    # ── SIT_ON_WINDOW ─────────────────────────────────
    def _update_sit_on_window(self):
        win = get_target_window()
        if win is None:
            self.state = FALL
            return

        _, wl, wt, wr, wb = win
        self.y = wt - self.pet_size

        self.x += self.facing * WALK_SPEED
        if self.x <= wl:
            self.x = wl
            self.facing = 1
        elif self.x >= wr - self.pet_size:
            self.x = wr - self.pet_size
            self.facing = -1

        if random.random() < 0.005:
            self.state = IDLE

    # ── WALK_ON_TASKBAR ───────────────────────────────
    def _update_walk_on_taskbar(self):
        taskbar = get_taskbar_rect()
        if taskbar is None:
            self.state = IDLE
            return

        tl, tt, tr, tb = taskbar
        self.y = tt - self.pet_size

        self.x += self.facing * WALK_SPEED
        if self.x <= tl:
            self.x = tl
            self.facing = 1
        elif self.x >= tr - self.pet_size:
            self.x = tr - self.pet_size
            self.facing = -1

        if random.random() < 0.003:
            self.state = IDLE

    # ── FALL ──────────────────────────────────────────
    def _update_fall(self):
        ground = self._ground_y()
        if self.y >= ground:
            self.y = ground
            self.state = IDLE
        else:
            self.y += FALL_SPEED

    # ── 工具 ──────────────────────────────────────────
    def _ground_y(self):
        taskbar = get_taskbar_rect()
        if taskbar:
            return taskbar[1] - self.pet_size
        _, sh = get_screen_size()
        return sh - self.pet_size - 40