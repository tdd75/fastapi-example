from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict

from app.dto.common_dto import BaseQueryDTO


class LocationQueryDTO(BaseQueryDTO):
    keyword: str | None = Query(None)


class LocationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field()
    name: str | None = Field()


class LocationListDTO(BaseModel):
    items: list[LocationDTO] = Field()
    total: int = Field()
