from fastapi import APIRouter,Depends, HTTPException,Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud.favorite import add_news_favorite, clear_list, get_list, is_news_favorite, remove_news_favorite


#ANCHOR - 创建router实例
router= APIRouter(prefix = "/api/favorite", tags =["favorite"])
# ————————————————————————————————————————


#ANCHOR - 查询收藏状态
@router.get('/check')
async def check_favorite(
   news_id:int = Query(...,alias='newsId'),
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   is_favorote = await is_news_favorite(db,news_id,user)
   return success_response(message="检查收藏状态成功",data=FavoriteCheckResponse(isFavorite=is_favorote))

#ANCHOR - 添加收藏
@router.post('/add')
async def add_favorite(
   data : FavoriteAddRequest,
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   
   # if check_favorite(data.news_id,user.id):
   #    return None
   # 因为有一致性约束，所以不用判断了
   
   res = await add_news_favorite(db, data.news_id, user)
   return success_response(message="添加收藏成功",data = res)

#ANCHOR - 取消收藏
@router.delete('/remove')
async def remove_favorite(
   news_id :int= Query(...,alias="newsId"),
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   result = await remove_news_favorite(db,news_id,user)
   if not result:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="收藏记录不存在")
   return success_response(message="取消收藏成功")


#ANCHOR - 获取收藏列表
@router.get('/list')
async def get_favorite_list(
   page:int = Query(1,ge = 1),
   page_size: int = Query(10,ge=1,le=100,alias="pageSize"),
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):

   # 这里有一个新用法！
   # 循环解包：用for按顺序赋值
   # 字典合并：**news.__dict__ 可以把数据库的一条全部拆散

   rows, total = await get_list(db, user.id, page, page_size)
   favorite_list = [{
      **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
   }for news, favorite_time, favorite_id in rows]
   has_more = total > page * page_size
   
   data = FavoriteListResponse(list = favorite_list,total=total,hasMore=has_more)
   return success_response(message = "获取收藏列表成功",data = data)


#ANCHOR - 清空收藏列表
@router.delete('/clear')
async def clear_favorite_list(
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   count = await clear_list(db,user.id)
   return success_response(message=f"清空了{count}条记录")  #NOTE - here!
