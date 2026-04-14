"""
behaviors/walk.py
"""
from api.windows_api import get_target_window
from .states import IDLE, CLIMB, WALK_SPEED


class WalkToWindowState:
    FRAME_KEY = "default"

    def enter(self, ctx) -> None:
        pass

    def update(self, ctx) -> str | None:
        win = get_target_window()
        if win is None:
            return IDLE

        _, wl, wt, wr, wb = win
        ctx._target_window = win

        ctx._climb_side = "left" if abs(ctx.x - wl) < abs(ctx.x - wr) else "right"
        target_x = wl if ctx._climb_side == "left" else wr - ctx.pet_size

        dx = target_x - ctx.x
        if abs(dx) < WALK_SPEED:
            ctx.x = target_x
            return CLIMB

        ctx.facing = 1 if dx > 0 else -1
        ctx.x += ctx.facing * WALK_SPEED
        ctx.y = ctx._ground_y()
        return None
