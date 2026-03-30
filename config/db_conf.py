from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from dotenv import load_dotenv
import os

# 1. 加载环境变量
load_dotenv()  

# 2. 从环境变量中读取配置
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 3. 动态拼接数据库 URL
# 使用 f-string 构造，这样代码里就不会出现明文密码了
ASYNC_DATABASE_URL = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,        # 可选：输出SQL日志
    pool_size =10,      # 设置连接池中保持的持久连接数
    max_overflow = 20   # 设置连接池允许创建的额外连接数(高峰时最多再多开 20 个，总共最多 30 个并发连接)
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_ = AsyncSession,
    expire_on_commit  =False #（负责管理每次请求的会话生命周期）
)

# 依赖项，用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()