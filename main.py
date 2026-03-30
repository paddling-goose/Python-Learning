from fastapi import FastAPI
from routers import history, news,users,favorite

from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # 允许跨域的源列表: 开发时允许所有
    allow_credentials=True,          # 允许携带 Cookie, 这个写true的时候，origins要写明确
    allow_methods=["*"],             # 允许所有的请求方法 (GET, POST 等)
    allow_headers=["*"],             # 允许所有的请求头
)

@app.get("/")
async def root():
    return {"message":"hello!hello!"}

# 挂载（注册）路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)