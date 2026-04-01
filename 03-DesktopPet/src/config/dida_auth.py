"""
dida_auth.py
滴答清单 OAuth2 授权模块（Password Grant）

流程：
  1. client_id / client_secret 从 .env 读取
  2. 弹出小窗口，用户填写滴答账号 + 密码
  3. 直接换取 access_token，不需要浏览器跳转
"""

import os
import tkinter as tk
from base64 import b64encode
from tkinter import messagebox

import requests
from dotenv import load_dotenv
from pathlib import Path

# 从脚本位置（src/config/）向上三级找到项目根目录的 .env
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# ── 常量 ──────────────────────────────────────────────────────────────────────
TOKEN_URL = "https://dida365.com/oauth/token"
SCOPE     = "tasks:read tasks:write"


# ── 登录弹窗 ──────────────────────────────────────────────────────────────────
def _ask_credentials() -> tuple[str, str] | None:
    """
    弹出一个小窗口，收集账号和密码。
    返回 (username, password)，用户点取消则返回 None。
    """
    result = {"username": None, "password": None}

    win = tk.Tk()
    win.title("滴答清单授权")
    win.resizable(False, False)
    win.eval("tk::PlaceWindow . center")   # 居中

    padding = {"padx": 12, "pady": 6}

    tk.Label(win, text="请输入滴答清单账号信息", font=("", 11, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(14, 4)
    )

    tk.Label(win, text="账号（邮箱/手机）").grid(row=1, column=0, sticky="e", **padding)
    entry_user = tk.Entry(win, width=28)
    entry_user.grid(row=1, column=1, **padding)
    entry_user.focus()

    tk.Label(win, text="密码").grid(row=2, column=0, sticky="e", **padding)
    entry_pass = tk.Entry(win, width=28, show="●")
    entry_pass.grid(row=2, column=1, **padding)

    def on_confirm(event=None):
        u = entry_user.get().strip()
        p = entry_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("提示", "账号和密码不能为空", parent=win)
            return
        result["username"] = u
        result["password"] = p
        win.destroy()

    def on_cancel():
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=(4, 14))
    tk.Button(btn_frame, text="取消", width=8, command=on_cancel).pack(side="left", padx=6)
    tk.Button(btn_frame, text="授权", width=8, command=on_confirm, default="active").pack(side="left", padx=6)

    # 回车也可以提交
    win.bind("<Return>", on_confirm)

    win.mainloop()

    if result["username"] is None:
        return None
    return result["username"], result["password"]


# ── 主类 ──────────────────────────────────────────────────────────────────────
class DidaAuth:
    """
    通过 Resource Owner Password Credentials (ROPC) Grant 获取 token。

    client_id / client_secret 优先从参数读取，否则从环境变量：
        DIDA_CLIENT_NAME
        DIDA_CLIENT_SECRET
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
    ):
        self.client_id     = client_id     or os.getenv("DIDA_CLIENT_NAME")
        self.client_secret = client_secret or os.getenv("DIDA_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "缺少 client_id / client_secret，"
                "请在 .env 设置 DIDA_CLIENT_NAME 和 DIDA_CLIENT_SECRET"
            )

    def _fetch_token(self, username: str, password: str) -> dict:
        credentials = b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        try:
            resp = requests.post(
                TOKEN_URL,
                headers={
                    "Authorization": f"Basic {credentials}",
                    "Content-Type":  "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "password",
                    "scope":      SCOPE,
                    "username":   username,
                    "password":   password,
                },
                timeout=10,
            )
            resp.raise_for_status()
        except requests.HTTPError:
            raise RuntimeError(
                f"登录失败：HTTP {resp.status_code}\n{resp.text}"
            )
        except requests.RequestException as e:
            raise RuntimeError(f"网络请求失败：{e}")

        data = resp.json()
        return {
            "access_token":  data["access_token"],
            "refresh_token": data.get("refresh_token"),
            "expires_in":    data.get("expires_in"),
        }

    def run(self) -> dict:
        """
        弹出登录窗口 → 获取 token dict。
        用户点取消则抛出 RuntimeError。
        """
        creds = _ask_credentials()
        if creds is None:
            raise RuntimeError("用户取消了授权")

        username, password = creds
        print("正在获取 token...")
        token = self._fetch_token(username, password)
        print("✅ 授权成功！")
        return token


# ── 直接运行 ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    auth  = DidaAuth()
    token = auth.run()
    print(f"\naccess_token  = {token['access_token'][:12]}...（已截断）")
    print(f"refresh_token = {token['refresh_token']}")
    print(f"expires_in    = {token['expires_in']}s")