import os
import json
import time
import threading
import webbrowser
import urllib.parse
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

import os
from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.getenv("DIDA_CLIENT_ID")
CLIENT_SECRET = os.getenv("DIDA_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"
TOKEN_FILE = "dida_token.json"

AUTH_URL = "https://dida365.com/oauth/authorize"
TOKEN_URL = "https://dida365.com/oauth/token"

# ── Token 本地缓存 ──────────────────────────────────────────

def save_token(token_data: dict):
    token_data["saved_at"] = time.time()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def load_token() -> dict | None:
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as f:
        return json.load(f)

def is_token_valid(token_data: dict) -> bool:
    expires_in = token_data.get("expires_in", 0)
    saved_at = token_data.get("saved_at", 0)
    return time.time() < saved_at + expires_in - 60  # 提前60秒刷新

# ── OAuth 授权码流程 ────────────────────────────────────────

_auth_code = None  # 回调拿到的 code

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        _auth_code = params.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("<h2>授权成功！可以关闭此页面 🎉</h2>".encode())

    def log_message(self, *args):
        pass  # 静默日志

def authorize() -> dict:
    """打开浏览器授权，本地监听回调，返回 token_data"""
    global _auth_code
    _auth_code = None

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "tasks:read",
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)
    webbrowser.open(url)

    # 启动本地服务器等待回调
    server = HTTPServer(("localhost", 8080), CallbackHandler)
    server.timeout = 120
    print("等待授权回调（最多120秒）...")
    server.handle_request()

    if not _auth_code:
        raise RuntimeError("未获取到授权码，请重试")

    # 用 code 换 token
    resp = requests.post(TOKEN_URL, data={
        "code": _auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }, auth=(CLIENT_ID, CLIENT_SECRET))
    resp.raise_for_status()
    token_data = resp.json()
    save_token(token_data)
    return token_data

def refresh_token(token_data: dict) -> dict:
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "refresh_token",
        "refresh_token": token_data["refresh_token"],
    }, auth=(CLIENT_ID, CLIENT_SECRET))
    resp.raise_for_status()
    new_token = resp.json()
    save_token(new_token)
    return new_token

def get_valid_token() -> str:
    """对外唯一入口：返回有效的 access_token"""
    token_data = load_token()
    if token_data is None:
        token_data = authorize()
    elif not is_token_valid(token_data):
        token_data = refresh_token(token_data)
    return token_data["access_token"]