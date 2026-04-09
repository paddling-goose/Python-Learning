import datetime
import requests
from api.dida.dida_auth import get_valid_token

API_BASE = "https://api.dida365.com/open/v1"


def _fetch_project_tasks(headers: dict, project_id: str) -> list[dict]:
    resp = requests.get(f"{API_BASE}/project/{project_id}/data", headers=headers)
    if resp.status_code != 200:
        return []
    return resp.json().get("tasks", [])


def get_today_tasks() -> list[dict]:
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    today = datetime.date.today().isoformat()

    # 拿所有项目 ID
    resp = requests.get(f"{API_BASE}/project", headers=headers)
    resp.raise_for_status()
    project_ids = [p["id"] for p in resp.json() if not p.get("closed")]

    # 收件箱单独加进去
    project_ids.append("inbox")

    today_tasks = []
    for pid in project_ids:
        for task in _fetch_project_tasks(headers, pid):
            if task.get("status", 0) == 2:   # 已完成，跳过
                continue
            due = (task.get("dueDate") or "")
            # 今天到期，或没有截止日期也列出来
            if (due and due[:10] <= today) or not due:
                today_tasks.append({
                    "title": task.get("title", "无标题"),
                    "priority": task.get("priority", 0),
                    "due": due[:10] if due else None,
                })

    today_tasks.sort(key=lambda t: -t["priority"])
    return today_tasks