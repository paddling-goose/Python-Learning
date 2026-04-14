import os
import json
import time
import threading
import webbrowser
import urllib.parse
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler


#ANCHOR - 获取env管理的敏感信息变量, 并定义 OAuth 相关常量
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("DIDA_CLIENT_ID")
CLIENT_SECRET = os.getenv("DIDA_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"
TOKEN_FILE = "dida_token.json"

#ANCHOR - 设置网络连接；NO_PROXY 表示不使用代理发送请求
AUTH_URL = "https://dida365.com/oauth/authorize"
TOKEN_URL = "https://dida365.com/oauth/token"
NO_PROXY = {"http": None, "https": None}


#ANCHOR - Token 本地缓存 


def save_token(token_data: dict):
    '''
    保存token到本地json

    Note:
        1. 使用 time.time() 自动更新 saved_at 字段
        2. with - 保证文件使用之后自动关闭
        3. w - 覆盖写，每次保存直接替换旧文件
        4. json.dump() - 把字典序列化写入文件;token_file的路径上面定义了
    
    Args:
        token_data: 
            包含 access_token、expires_in、expires_in 的字典
            由该函数添加  saved_at 字段  
    '''

    token_data["saved_at"] = time.time()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    


def load_token() -> dict | None:
    '''
    加载本地保存的token

    Notes:
        1. is token_file exists? load : return None
        2. 先用with open一个文件，之后再选择对应操作（这里是 load ）
        3. -> - 标注的是函数的返回类型
    '''
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as f:
        return json.load(f)


def is_token_valid(token_data: dict) -> bool:
    '''
    判断token是否有效
    
    Notes：
        1. 比较保存日期和过期时间，提前60秒刷新
        2. token_data.get() - 直接用因为直接用 token_data["expires_in"] 在键不存在时会抛出 KeyError, 程序直接崩溃
            使用get ：键不存在时返回默认值
        3. 默认指给0的兜底效果： time.time() < 0 + 0 - 60  # → False
 
    Returns:
        True 表示 token 有效，False 表示需要刷新。
    '''
    expires_in = token_data.get("expires_in", 0)  # 键不存在时返回默认值0
    saved_at = token_data.get("saved_at", 0)
    return time.time() < saved_at + expires_in - 60  # 提前60秒刷新


#ANCHOR - OAuth 授权码流程

_auth_code = None  # 回调拿到的 code

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''

        用户在浏览器授权后，滴答清单会把浏览器重定向
        1. 解析新网页
        2. 成功后返回通知

        Note：
            1. 读取全局变量不需要声明，修改全局变量必须声明 global
            2. urlparse - 解析 URL，提取查询参数
            3. parse_qs - 把查询字符串解析成字典，值是列表
            4. get("code", [None])[0] - code[0]; 没有 code 则None

            5. end_headers - HTTP 协议要求: Header 写完后，必须有一个空行，然后再写 Body
            6. self - 指实例对象；类方法中第一个参数恒给self
        '''
        global _auth_code  # 用全局变量需要声明
        parsed = urllib.parse.urlparse(self.path)  # → "/callback?code=ABC123&state=xyz"
        params = urllib.parse.parse_qs(parsed.query)  # -> { "code": ["ABC123"], "state": ["xyz"] }
        _auth_code = params.get("code", [None])[0] 
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("<h2>授权成功！可以关闭此页面 🎉</h2>".encode())  # .encode() 是把字符串转成 bytes，因为 HTTP 传输的是字节流。

    def log_message(self, *args):
        pass  # 静默日志，保持控制台清爽

#ANCHOR - 其余操作

def authorize() -> dict:
    """
    打开浏览器授权，本地监听回调，返回 token_data
    
    Notes：
        1. 利用 resp.raise_for_status 处理错误信息
        2. 启动本地服务器的操作：
            1. HTTPServer - 在本地电脑搭建临时网站
            2. server.timeout = 120 - 设置时间上线，防止死锁
            3. server.handle_request - 阻塞运行，只有完成 OAuth 授权处理才继续运行
    """
    global _auth_code
    _auth_code = None

    # 这里依照 dida 官方文档写
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
    resp = requests.post(
        TOKEN_URL, 
        data={
            "code": _auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }, 
        auth=(CLIENT_ID, CLIENT_SECRET),
        proxies=NO_PROXY,
    )
    resp.raise_for_status()  # 如果 HTTP 状态码是 4xx/5xx 就抛异常
    token_data = resp.json()  # 解析响应体为字典
    save_token(token_data)  # 缓存到本地文件
    return token_data


def refresh_token(token_data: dict) -> dict:
    '''静默刷新token'''
    resp = requests.post(
        TOKEN_URL, 
        data={  
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"],
        }, 
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
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
    return token_data["access_token"]  # 通过键名获取对应的值