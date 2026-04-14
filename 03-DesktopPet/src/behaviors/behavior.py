"""
behaviors/behavior.py
"""
from .base   import BaseMovement
from .states import IDLE, WALK_TO_WINDOW, CLIMB, SIT_ON_WINDOW, WALK_ON_TASKBAR, FALL
from .chat   import Chat
from .alert  import Alert


class Behavior:
    def __init__(self, pet_size: int):
        self.movement = BaseMovement(pet_size)
        self.chat     = Chat()
        self.alert    = Alert()
        self.state    = IDLE

    @property
    def frame_key(self) -> str:
        """透传：pet.py 从这里读，不需要知道 BaseMovement 的存在。"""
        return self.movement.frame_key

    def enable_dida(self, get_tasks_fn) -> None:
        self.alert.enable_dida(get_tasks_fn)

    def update(self) -> tuple[int, int, str]:
        x, y, state = self.movement.update()
        self.state = state
        return x, y, state

    def get_alert(self) -> str | None:
        return self.alert.tick()

    def set_position(self, x: int, y: int) -> None:
        self.movement.set_position(x, y)
        self.state = IDLE

    def greet(self)            -> str: return self.chat.greet()
    def idle_message(self)     -> str: return self.chat.idle_message()
    def reply(self, text: str) -> str: return self.chat.reply(text)

    def go_climb(self):   self.movement.go_to(WALK_TO_WINDOW)
    def go_taskbar(self): self.movement.go_to(WALK_ON_TASKBAR)
    def go_idle(self):    self.movement.go_to(IDLE)
