import datetime
import requests
from api.dida.dida_auth import get_valid_token

NO_PROXY = {"http": None, "https": None}
API_BASE = "https://api.dida365.com/open/v1"


def _get_headers() -> dict:
    """
    从 dida_auth模块获取有效的token，构造并返回HTTP请求头
    """
    token = get_valid_token()
    return {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
    }


def _fetch_project_tasks(headers: dict, project_id: str) -> list[dict]:
    """
    根据项目id拉取该项目下所有任务
    """
    resp = requests.get(
        f"{API_BASE}/project/{project_id}/data",
        headers=headers, 
        proxies=NO_PROXY,
    )
    if resp.status_code != 200:
        return []
    return resp.json().get("tasks", [])

#ANCHOR - 公开业务函数

def get_all_projects() -> list[dict]:
    """
    返回所有未关闭的项目列表，格式：
        [{"id": "...", "name": "..."}, ...]
    收件箱固定追加在最后。
    """
    headers = _get_headers()
    resp = requests.get(
        f"{API_BASE}/project",
        headers=headers, 
        proxies=NO_PROXY
    )
    resp.raise_for_status()
    projects = [
        {"id": p["id"], "name": p.get("name", "未命名")}
        for p in resp.json()
        if not p.get("closed")
    ]
    projects.append({"id": "inbox", "name": "收件箱"})
    return projects


def get_today_tasks(selected_project_ids: list[str] | None = None) -> list[dict]:
    """
    返回今日到期的未完成任务。

    params:
        selected_project_ids: 要检查的项目 ID 列表；
                            传 None 时退化为原来的行为（检查全部项目）。
    """
    headers = _get_headers()
    today = datetime.date.today().isoformat()

    if selected_project_ids is None:
        # 未配置时拉取全部项目（兼容旧行为）
        resp = requests.get(f"{API_BASE}/project", headers=headers, proxies=NO_PROXY)
        resp.raise_for_status()
        selected_project_ids = [
            p["id"] for p in resp.json() if not p.get("closed")
        ]
        selected_project_ids.append("inbox")

    today_tasks = []
    for pid in selected_project_ids:
        for task in _fetch_project_tasks(headers, pid):
            if task.get("status", 0) == 2:
                continue
            due = task.get("dueDate") or ""
            if due and due[:10] <= today:
                today_tasks.append({
                    "title":    task.get("title", "无标题"),
                    "priority": task.get("priority", 0),
                    "due":      due[:10],
                })

    today_tasks.sort(key=lambda t: -t["priority"])
    return today_tasks