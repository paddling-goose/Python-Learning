# 整合 根据 Token 查询用户，返回用户

from fastapi import Depends, Header,HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import users

async def get_current_user(
        authorization:str = Header(...,lias="Authorization"),
        db : AsyncSession = Depends(get_db)
):
    #NOTE - 这里需要整理token
    token = authorization #split(" ")[1]
    # 或写作： token = authorization("Bearer"，"")
    user = await users.get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效令牌或令牌过期")
    
    return user