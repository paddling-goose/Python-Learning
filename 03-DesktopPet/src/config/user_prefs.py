"""
config/user_prefs.py
用户偏好持久化（目前只存滴答项目过滤列表）。
数据保存在项目根目录的 user_prefs.json。
"""
import os
import json

_PREFS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "user_prefs.json",
)


def _load() -> dict:
    if not os.path.exists(_PREFS_FILE):
        return {}
    with open(_PREFS_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(_PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 滴答项目过滤 ─────────────────────────────────────────────────────────── #

def get_selected_project_ids() -> list[str] | None:
    """
    返回用户勾选的项目 ID 列表。
    若用户从未设置过，返回 None（调用方应当检查全部项目）。
    """
    data = _load()
    return data.get("selected_project_ids", None)


def save_selected_project_ids(ids: list[str]) -> None:
    data = _load()
    data["selected_project_ids"] = ids
    _save(data)