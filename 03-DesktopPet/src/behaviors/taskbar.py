"""
behaviors/taskbar.py
"""
import random
from api.windows_api import get_taskbar_rect
from .states import IDLE, WALK_SPEED

_LEAVE_PROB = 0.003


class TaskbarState:
    FRAME_KEY = "default"

    def enter(self, ctx) -> None:
        pass

    def update(self, ctx) -> str | None:
        taskbar = get_taskbar_rect()
        if taskbar is None:
            return IDLE

        tl, tt, tr, tb = taskbar
        ctx.y = tt - ctx.pet_size

        ctx.x += ctx.facing * WALK_SPEED
        if ctx.x <= tl:
            ctx.x = tl
            ctx.facing = 1
        elif ctx.x >= tr - ctx.pet_size:
            ctx.x = tr - ctx.pet_size
            ctx.facing = -1

        if random.random() < _LEAVE_PROB:
            return IDLE
        return None
