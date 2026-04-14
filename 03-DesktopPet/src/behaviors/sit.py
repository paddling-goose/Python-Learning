"""
behaviors/sit.py
"""
import random
from api.windows_api import get_target_window
from .states import FALL, IDLE, WALK_SPEED

_LEAVE_PROB = 0.005


class SitOnWindowState:
    FRAME_KEY = "sit"

    def enter(self, ctx) -> None:
        pass

    def update(self, ctx) -> str | None:
        win = get_target_window()
        if win is None:
            return FALL

        _, wl, wt, wr, wb = win
        ctx.y = wt - ctx.pet_size

        ctx.x += ctx.facing * WALK_SPEED
        if ctx.x <= wl:
            ctx.x = wl
            ctx.facing = 1
        elif ctx.x >= wr - ctx.pet_size:
            ctx.x = wr - ctx.pet_size
            ctx.facing = -1

        if random.random() < _LEAVE_PROB:
            return IDLE
        return None
