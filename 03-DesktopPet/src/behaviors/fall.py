"""
behaviors/fall.py
"""
from .states import IDLE, FALL_SPEED


class FallState:
    FRAME_KEY = "default"

    def enter(self, ctx) -> None:
        pass

    def update(self, ctx) -> str | None:
        ground = ctx._ground_y()
        if ctx.y >= ground:
            ctx.y = ground
            return IDLE
        ctx.y += FALL_SPEED
        return None
