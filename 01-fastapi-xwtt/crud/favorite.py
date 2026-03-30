from sqlalchemy import delete, select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News
from models.users import User
from models.favourite import Favorite

async def is_news_favorite(
        db:AsyncSession,
        news_id:int,
        user:User
):
    stmt = select(Favorite).where(Favorite.news_id == news_id , Favorite.user_id ==user.id )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None  #FIXME - 这是啥


async def add_news_favorite(
        db:AsyncSession,
        news_id:int,
        user:User
):
    new_favorite = Favorite(news_id = news_id,user_id = user.id)
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)
    return new_favorite


async def remove_news_favorite(
        db:AsyncSession,
        news_id:int,
        user:User
):
    stmt = delete(Favorite).where(Favorite.news_id == news_id , Favorite.user_id ==user.id)
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
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()


    #[
    #  (新闻对象，收藏时间，收藏id)
    #]

    offset =(page-1) * page_size
    #NOTE - 这里有两种分行方式：在末尾\ 或 加括号
    stmt = (select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
            .join(Favorite, Favorite.news_id == News.id)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
            .offset(offset).limit(page_size)
            )

    result = await db.execute(stmt)
    rows = result.all()
    return rows,total

async def clear_list(
        db: AsyncSession, 
        user_id:int, 
):
    stmt = delete(Favorite).where(Favorite.user_id==user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount  or 0   #NOTE 