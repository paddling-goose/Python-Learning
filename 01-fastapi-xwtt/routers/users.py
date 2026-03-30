from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_conf import get_db

from crud import users
from models.users import User
from schemas.users import UserChangePasswordRequest, UserRequest,UserAuthResponse,UserInfoResponse, UserUpdateRequest
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix = "/api/user", tags =["users"])

#ANCHOR - 用户注册
@router.post("/register")
async def register(user_data: UserRequest ,db:AsyncSession =Depends(get_db)):
    # NOTE logic: regist-> if not exist -> create token -> return response
    existing_user = await users.get_user_by_username(db,user_data.username)

    if(existing_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    user = await users.create_user(db,user_data)
    token = await users.create_token(db,user.id)
#     return {
#         "code": 200,
#         "message": "注册成功",
#         "data": {
#             "token": token,
#             "userInfo": {
#                 "id": user.id,
#                 "username": user.username,
#                 "bio": user.bio,
#                 "avatar": user.avatar
#             }
#     }
# }
    response_data = UserAuthResponse(token=token.token,user_info= UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)

#ANCHOR - 用户登入
@router.post("/login")
async def login(user_data: UserRequest ,db:AsyncSession =Depends(get_db)):
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户名或密码错误")
    
    token = await users.create_token(db,user.id)
    response_data = UserAuthResponse(token=token.token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=response_data)

#ANCHOR - 获取用户信息
#NOTE -查token -> 封装crud -> 整合成工具函数 -> 路由依赖注入
@router.get("/info")
async def get_user_infodata(user:User= Depends(get_current_user)):
    return success_response(message="用户信息获取成功",data=UserInfoResponse.model_validate(user))

#ANCHOR - 修改用户信息
# 包含用户输入，还要用户token，还要db
@router.put("/update")
async def update_user_info(
    user_data: UserUpdateRequest,
    user:User = Depends(get_current_user),
    db:AsyncSession =Depends(get_db)
):
    try:
        user = await users.update_user(db, user.username, user_data)
        return success_response(message="修改成功", data=UserInfoResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

#ANCHOR - 修改用户密码
#流程： 判断旧密码是否正确（verify）-> 加密新密码 -> 提交新密码
@router.put('/password')
async def update_password(
    password_data:UserChangePasswordRequest,
    user : User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res_change_pwd = await users.change_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change_pwd:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="旧密码错误")
    return success_response(message="密码修改成功")