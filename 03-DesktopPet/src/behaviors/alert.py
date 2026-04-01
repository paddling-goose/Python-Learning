"""
alert.py
提醒系统
现在：定时随机提醒
未来：接入滴答清单，读取今日任务并按时提醒
"""
import time
import random
from datetime import datetime


# ── 内置提醒（不需要滴答清单也能用）────────────────────
BUILTIN_REMINDERS = [
    "喝水时间到！💧",
    "起来活动一下吧🧘",
    "该休息眼睛了👀",
    "记得吃饭哦🍱",
]


class Alert:
 
    def __init__(self):
        self._tasks = []          # 未来：从滴答清单读取的任务列表
        self._last_check = 0      # 上次检查时间戳
        self._check_interval = 60 # 每60秒检查一次（秒）
        self._dida = None         # 未来：滴答清单 API 实例

    def tick(self) -> str | None:
        """
        每帧调用，到时间返回提醒文字，否则返回 None
        """
        now = time.time()
        if now - self._last_check < self._check_interval:
            return None

        self._last_check = now
        return self._check_alerts()

    def _check_alerts(self) -> str | None:
        # ── 未来接入滴答清单的位置 ────────────────────
        # if self._dida:
        #     tasks = self._dida.get_due_tasks()
        #     for task in tasks:
        #         if self._is_due_now(task):
        #             return f"⏰ {task['title']}"
        # ─────────────────────────────────────────────

        # 现在：随机触发内置提醒（30% 概率）
        if random.random() < 0.3:
            return random.choice(BUILTIN_REMINDERS)
        return None

    def _is_due_now(self, task: dict) -> bool:
        """判断任务是否到期（未来用）"""
        due = task.get("dueDate")
        if not due:
            return False
        due_time = datetime.fromisoformat(due)
        now = datetime.now()
        diff = (due_time - now).total_seconds()
        return 0 <= diff <= self._check_interval

    def enable_dida(self, access_token: str):
        """
        开启滴答清单模式（未来调用这个方法激活）
        """
        # TODO: 初始化 dida_api
        # from api.dida_api import DidaAPI
        # self._dida = DidaAPI(access_token)
        pass