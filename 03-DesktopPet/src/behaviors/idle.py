"""
behaviors/idle.py
"""
import random
from .states import WALK_TO_WINDOW, WALK_ON_TASKBAR


class IdleState:
    FRAME_KEY = "default"

    def enter(self, ctx) -> None:
        ctx._idle_timer = 0

    def update(self, ctx) -> str | None:
        ctx._idle_timer += 1
        if ctx._idle_timer > random.randint(180, 360):
            return random.choices(
                [WALK_TO_WINDOW, WALK_ON_TASKBAR],
                weights=[70, 30],
            )[0]
        return None
