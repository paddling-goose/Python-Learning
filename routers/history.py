from fastapi import APIRouter,Depends, HTTPException,Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud.history import add_view_history, get_list, clear_list, remove_view_history


#ANCHOR - 创建router实例
router= APIRouter(prefix = "/api/history", tags =["history"])
# ————————————————————————————————————————


#ANCHOR - 添加浏览记录
@router.post('/add')
async def add_history(
   data : HistoryAddRequest,
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   res = await add_view_history(db, data.news_id, user)
   return success_response(message="添加浏览记录成功",data = res)

#ANCHOR - 删除单条浏览记录
@router.delete('/delete/{news_id}')
async def remove_history(
   news_id :int,  #FIXME -  query和{}只能选一个
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   result = await remove_view_history(db,news_id,user)
   if not result:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="浏览记录不存在")
   return success_response(message="删除浏览记录成功")


#ANCHOR - 获取浏览历史列表
@router.get('/list')
async def get_history_list(
   page:int = Query(1,ge = 1),
   page_size: int = Query(10,ge=1,le=100,alias="pageSize"),
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):

   # 这里有一个新用法！
   # 循环解包：用for按顺序赋值
   # 字典合并：**news.__dict__ 可以把数据库的一条全部拆散

   rows, total = await get_list(db, user.id, page, page_size)
   history_list = [{
      **news.__dict__,
        "view_time": view_time,
        "history_id": history_id
   }for news, view_time,history_id, in rows]
   has_more = total > page * page_size
   
   data = HistoryListResponse(list = history_list,total=total,hasMore=has_more)
   return success_response(message = "获取浏览历史列表成功",data = data)


#ANCHOR - 清空浏览历史列表
@router.delete('/clear')
async def clear_hitory_list(
   user: User = Depends(get_current_user),
   db: AsyncSession = Depends(get_db)
):
   count = await clear_list(db,user.id)
   return success_response(message=f"清空了{count}条记录")  #NOTE - here!
