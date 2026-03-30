from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
    news_id:int = Field(...,alias="newsId")
    

class HistoryNewsItemResponse(NewsItemBase):
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


# 收藏列表接口响应模型类
class  HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total:int
    hasMore: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )