import time, random
from datetime import datetime

BUILTIN_REMINDERS = ["喝水时间到！💧", "起来活动一下吧🧘", "该休息眼睛了👀", "记得吃饭哦🍱"]


class Alert:
    def __init__(self):
        self._get_tasks = None    # 注入的任务获取函数
        self._last_check = 0
        self._check_interval = 60

    def enable_dida(self, get_tasks_fn):
        """
        注入任务获取函数，解耦 token 管理
        用法：alert.enable_dida(dida_tasks.get_today_tasks)
        """
        self._get_tasks = get_tasks_fn

    def tick(self) -> str | None:
        now = time.time()
        if now - self._last_check < self._check_interval:
            return None
        self._last_check = now
        return self._check_alerts()

    def _check_alerts(self) -> str | None:
        if self._get_tasks:
            try:
                tasks = self._get_tasks()
                due = [t for t in tasks if self._is_due_now(t)]
                if due:
                    return f"⏰ {due[0]['title']}"
            except Exception as e:
                print(f"[Alert] 获取任务失败: {e}")

        if random.random() < 0.3:
            return random.choice(BUILTIN_REMINDERS)
        return None

    def _is_due_now(self, task: dict) -> bool:
        due = task.get("dueDate")
        if not due:
            return False
        due_time = datetime.fromisoformat(due)
        diff = (due_time - datetime.now()).total_seconds()
        return 0 <= diff <= self._check_interval