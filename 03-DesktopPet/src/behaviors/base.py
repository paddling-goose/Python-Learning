"""
behaviors/base.py
BaseMovement —— 调度器，同时透传 frame_key 给上层。
"""
from api.windows_api import get_taskbar_rect, get_screen_size

from .states  import (
    IDLE, WALK_TO_WINDOW, CLIMB, SIT_ON_WINDOW, WALK_ON_TASKBAR, FALL,
    WALK_SPEED, CLIMB_SPEED, FALL_SPEED,
)
from .idle    import IdleState
from .walk    import WalkToWindowState
from .climb   import ClimbState
from .sit     import SitOnWindowState
from .taskbar import TaskbarState
from .fall    import FallState


class BaseMovement:
    _HANDLERS: dict = {
        IDLE:            IdleState(),
        WALK_TO_WINDOW:  WalkToWindowState(),
        CLIMB:           ClimbState(),
        SIT_ON_WINDOW:   SitOnWindowState(),
        WALK_ON_TASKBAR: TaskbarState(),
        FALL:            FallState(),
    }

    def __init__(self, pet_size: int):
        self.pet_size   = pet_size
        self.state      = IDLE
        self.x          = 100
        self.y          = 100
        self.facing     = 1

        self._idle_timer    = 0
        self._target_window = None
        self._climb_side    = "left"

        self._HANDLERS[self.state].enter(self)

    def update(self) -> tuple[int, int, str]:
        next_state = self._HANDLERS[self.state].update(self)
        if next_state is not None and next_state != self.state:
            self._switch_to(next_state)
        return self.x, self.y, self.state

    @property
    def frame_key(self) -> str:
        """当前状态对应的图片集名称，直接读状态类上的声明。"""
        return self._HANDLERS[self.state].FRAME_KEY

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self._switch_to(IDLE)

    def go_to(self, state: str) -> None:
        self._switch_to(state)

    def _switch_to(self, state: str) -> None:
        self.state = state
        self._HANDLERS[state].enter(self)

    def _ground_y(self) -> int:
        taskbar = get_taskbar_rect()
        if taskbar:
            return taskbar[1] - self.pet_size
        _, sh = get_screen_size()
        return sh - self.pet_size - 40
