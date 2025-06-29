from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict

from app.dto.common_dto import BaseQueryDTO


class DepartmentQueryDTO(BaseQueryDTO):
    keyword: str | None = Query()


class DepartmentDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field()
    name: str | None = Field()


class DepartmentListDTO(BaseModel):
    items: list[DepartmentDTO] = Field()
    total: int = Field()
