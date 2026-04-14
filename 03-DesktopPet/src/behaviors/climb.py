"""
behaviors/climb.py
"""
from api.windows_api import get_target_window
from .states import FALL, SIT_ON_WINDOW, CLIMB_SPEED


class ClimbState:
    FRAME_KEY = "climb"

    def enter(self, ctx) -> None:
        pass

    def update(self, ctx) -> str | None:
        win = get_target_window()
        if win is None:
            return FALL

        _, wl, wt, wr, wb = win
        ctx.x = wl if ctx._climb_side == "left" else wr - ctx.pet_size

        target_y = wt - ctx.pet_size
        if ctx.y - target_y < CLIMB_SPEED:
            ctx.y = target_y
            ctx._target_window = win
            return SIT_ON_WINDOW

        ctx.y -= CLIMB_SPEED
        return None
