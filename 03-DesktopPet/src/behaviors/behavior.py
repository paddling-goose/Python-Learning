"""
behavior.py
总调度器，把 base / chat / alert 组合起来
pet.py 只需要和这个文件交互
"""
from behaviors.base  import BaseMovement, IDLE, WALK_TO_WINDOW, WALK_ON_TASKBAR
from behaviors.chat  import Chat
from behaviors.alert import Alert

# 把状态常量也暴露出去，方便 pet.py 直接从这里导入
from behaviors.base import (
    IDLE, WALK_TO_WINDOW, CLIMB,
    SIT_ON_WINDOW, WALK_ON_TASKBAR, FALL
)


class Behavior:
    """
    桌宠大脑，统一对外接口
    pet.py 用法：
        self.behavior = Behavior(PET_SIZE)
        x, y, state = self.behavior.update()
        msg = self.behavior.get_message()
    """

    def __init__(self, pet_size):
        self.movement = BaseMovement(pet_size)
        self.chat     = Chat()
        self.alert    = Alert()

        self.state    = IDLE

    # ── 每帧调用 ──────────────────────────────────────
    def update(self):
        """更新移动，返回 (x, y, state)"""
        x, y, state = self.movement.update()
        self.state = state
        return x, y, state

    def get_alert(self) -> str | None:
        """检查是否有提醒要弹出，有则返回文字"""
        return self.alert.tick()

    # ── 位置同步 ──────────────────────────────────────
    def set_position(self, x, y):
        self.movement.set_position(x, y)
        self.state = IDLE

    # ── 消息 ──────────────────────────────────────────
    def greet(self) -> str:
        return self.chat.greet()

    def idle_message(self) -> str:
        return self.chat.idle_message()

    def reply(self, user_input: str) -> str:
        return self.chat.reply(user_input)

    # ── 手动触发行为 ──────────────────────────────────
    def go_climb(self):
        self.movement.go_to(WALK_TO_WINDOW)

    def go_taskbar(self):
        self.movement.go_to(WALK_ON_TASKBAR)

    def go_idle(self):
        self.movement.go_to(IDLE)