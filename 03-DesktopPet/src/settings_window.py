"""
src/settings_window.py
设置窗口：从滴答拉取项目列表，用户勾选后保存。
"""
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from config.user_prefs import get_selected_project_ids, save_selected_project_ids


class SettingsWindow:
    def __init__(self, parent: tk.Tk):
        self._parent = parent
        self._win: tk.Toplevel | None = None

    def open(self) -> None:
        """打开设置窗口，若已打开则聚焦。"""
        if self._win and self._win.winfo_exists():
            self._win.lift()
            return

        win = tk.Toplevel(self._parent)
        self._win = win
        win.title("设置 · 滴答提醒项目")
        win.resizable(False, False)
        win.grab_set()   # 模态

        # ── 标题 ────────────────────────────────────────────────────── #
        tk.Label(win, text="选择要提醒的项目", font=("", 12, "bold"),
                 pady=10).pack()
        tk.Label(win, text="只有勾选项目中今日到期的任务会弹出提醒",
                 fg="gray").pack()

        # ── 加载动画区 ───────────────────────────────────────────────── #
        status_var = tk.StringVar(value="正在获取项目列表…")
        status_label = tk.Label(win, textvariable=status_var, fg="gray")
        status_label.pack(pady=4)

        # ── 列表区（带滚动条）────────────────────────────────────────── #
        frame = tk.Frame(win)
        frame.pack(padx=20, pady=4, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self._listbox_frame = tk.Frame(frame)
        self._listbox_frame.pack(side="left", fill="both", expand=True)

        # ── 按钮区 ───────────────────────────────────────────────────── #
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)

        self._save_btn = tk.Button(btn_frame, text="保存", width=10,
                                   state="disabled",
                                   command=self._on_save)
        self._save_btn.pack(side="left", padx=6)

        tk.Button(btn_frame, text="取消", width=10,
                  command=win.destroy).pack(side="left", padx=6)

        self._vars: dict[str, tk.BooleanVar] = {}   # project_id → BooleanVar
        self._projects: list[dict] = []

        # 后台线程拉取项目列表，避免卡 UI
        threading.Thread(
            target=self._fetch_projects,
            args=(status_var, status_label),
            daemon=True,
        ).start()

    # ── 后台：拉取项目 ────────────────────────────────────────────────── #

    def _fetch_projects(self, status_var: tk.StringVar,
                        status_label: tk.Label) -> None:
        try:
            from api.dida.dida_tasks import get_all_projects
            projects = get_all_projects()
        except Exception as e:
            self._parent.after(0, lambda e=e: status_var.set(f"获取失败：{e}"))
            return

        self._projects = projects
        self._parent.after(0, lambda: self._render_projects(
            projects, status_var, status_label))

    # ── 主线程：渲染勾选框 ────────────────────────────────────────────── #

    def _render_projects(self, projects: list[dict],
                         status_var: tk.StringVar,
                         status_label: tk.Label) -> None:
        status_label.pack_forget()

        selected_ids = get_selected_project_ids()
        # 未曾设置过 → 默认全部勾选
        all_selected = selected_ids is None

        for p in projects:
            var = tk.BooleanVar(value=all_selected or p["id"] in selected_ids)
            self._vars[p["id"]] = var
            tk.Checkbutton(
                self._listbox_frame,
                text=p["name"],
                variable=var,
                anchor="w",
                width=28,
            ).pack(fill="x", pady=1)

        self._save_btn.config(state="normal")

        # 全选 / 全不选快捷按钮
        quick_frame = tk.Frame(self._win)
        quick_frame.pack(before=self._listbox_frame.master)
        tk.Button(quick_frame, text="全选", font=("", 8),
                  command=self._select_all).pack(side="left", padx=4)
        tk.Button(quick_frame, text="全不选", font=("", 8),
                  command=self._deselect_all).pack(side="left")

    # ── 保存 ─────────────────────────────────────────────────────────── #

    def _on_save(self) -> None:
        selected = [pid for pid, var in self._vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("提示", "至少选择一个项目", parent=self._win)
            return
        save_selected_project_ids(selected)
        messagebox.showinfo("已保存",
                            f"已选择 {len(selected)} 个项目，下次提醒生效",
                            parent=self._win)
        self._win.destroy()

    # ── 快捷操作 ─────────────────────────────────────────────────────── #

    def _select_all(self) -> None:
        for var in self._vars.values():
            var.set(True)

    def _deselect_all(self) -> None:
        for var in self._vars.values():
            var.set(False)