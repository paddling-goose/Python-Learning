from behaviors.base import (
    BaseMovement,
    IDLE, WALK_TO_WINDOW, CLIMB, SIT_ON_WINDOW, WALK_ON_TASKBAR, FALL
)
from behaviors.chat import Chat
from behaviors.alert import Alert


class Behavior:
    def __init__(self, pet_size):
        self.movement = BaseMovement(pet_size)
        self.chat = Chat()
        self.alert = Alert()
        self.state = IDLE

    def enable_dida(self, get_tasks_fn):
        """main.py 完成 OAuth 后调用这个激活滴答提醒"""
        self.alert.enable_dida(get_tasks_fn)

    def update(self):
        x, y, state = self.movement.update()
        self.state = state
        return x, y, state

    def get_alert(self) -> str | None:
        return self.alert.tick()

    def set_position(self, x, y):
        self.movement.set_position(x, y)
        self.state = IDLE

    def greet(self) -> str:        return self.chat.greet()
    def idle_message(self) -> str: return self.chat.idle_message()
    def reply(self, text: str) -> str: return self.chat.reply(text)

    def go_climb(self):   self.movement.go_to(WALK_TO_WINDOW)
    def go_taskbar(self): self.movement.go_to(WALK_ON_TASKBAR)
    def go_idle(self):    self.movement.go_to(IDLE)