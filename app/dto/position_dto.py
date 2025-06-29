from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict

from app.dto.common_dto import BaseQueryDTO


class PositionQueryDTO(BaseQueryDTO):
    keyword: str | None = Query(None)


class PositionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field()
    title: str | None = Field()


class PositionListDTO(BaseModel):
    items: list[PositionDTO] = Field()
    total: int = Field()
