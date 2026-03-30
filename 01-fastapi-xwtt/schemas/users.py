from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# FIXME what is basemodel??
class UserRequest(BaseModel):
    username: str
    password: str


# userInfo 对应的类： 基础类型
class UserInfoBase(BaseModel):
    nickname:Optional[str] = Field(None,max_length =50, alias="昵称")
    avatar:Optional[str] = Field(None,max_length =255, alias="头像URL")
    gender:Optional[str] = Field(None,max_length=10,alias="性别")
    bio:Optional[str] = Field(None,max_length=500,alias="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  
    )

# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse= Field(...,alias="userInfo") # 起一个别名; ...表示这个字段是必填的

    # 模型类配置
    model_config = ConfigDict(
       populate_by_name= True,  # alias/字段名兼容用
       from_attributes= True    # 允许从ORM 字段中取值
    )
    
#ANCHOR - 更新用户信息 
class UserUpdateRequest(BaseModel):
    nickname:Optional[str] = Field(None,max_length =50, alias="昵称")
    avatar:Optional[str] = Field(None,max_length =255, alias="头像URL")
    gender:Optional[str] = Field(None,max_length=10,alias="性别")
    bio:Optional[str] = Field(None,max_length=500,alias="个人简介")
    phone: Optional[str] = Field(None, max_length=20)


#ANCHOR - 修改用户密码
class UserChangePasswordRequest(BaseModel):
    old_password :str = Field(...,alias= "oldPassword",description="旧密码")
    new_password: str = Field(...,max_length=50,alias="newPassword",description="新密码")
