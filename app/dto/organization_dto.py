from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict

from app.dto.common_dto import BaseQueryDTO


class OrganizationQueryDTO(BaseQueryDTO):
    keyword: str | None = Query(None)


class OrganizationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field()
    name: str | None = Field()


class OrganizationListDTO(BaseModel):
    items: list[OrganizationDTO] = Field()
    total: int = Field()
