from datetime import datetime

from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News
from models.users import User
from models.history import History


async def add_view_history(db: AsyncSession, news_id: int, user: User):
    result = await db.execute(
        select(History).where(
            History.user_id == user.id,
            History.news_id == news_id
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.view_time = datetime.now()
        await db.commit()
        return existing
    else:
        new_history = History(user_id=user.id, news_id=news_id)
        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)  # ✅ 只在新插入时 refresh
        return new_history
            


async def remove_view_history(
        db:AsyncSession,
        news_id:int,
        user:User
):
    stmt = delete(History).where(History.news_id == news_id , History.user_id ==user.id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_list(
        db: AsyncSession, 
        user_id:int, 
        page:int =1,
        page_size:int = 10
):
    # 需要：总量 + 收藏列表list
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()


    #[
    #  (新闻对象，浏览时间，浏览历史id)
    #]

    offset =(page-1) * page_size
    #NOTE - 这里有两种分行方式：在末尾\ 或 加括号
    stmt = (select(News,History.view_time,History.id.label("history_id"))
            .join(History, History.news_id == News.id)
            .where(History.user_id == user_id)
            .order_by(History.view_time.desc())
            .offset(offset).limit(page_size)
            )

    result = await db.execute(stmt)
    rows = result.all()
    return rows,total

async def clear_list(
        db: AsyncSession, 
        user_id:int, 
):
    stmt = delete(History).where(History.user_id==user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount  or 0   #NOTE 