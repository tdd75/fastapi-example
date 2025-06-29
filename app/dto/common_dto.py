from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app import setting


class BaseQueryDTO(BaseModel):
    limit: int = Query(10)
    offset: int = Query(0)

    @model_validator(mode='after')
    def validate_limit(self):
        if self.limit > setting.MAX_PAGE_SIZE:
            raise ValueError(f'Limit cannot be greater than {setting.Setting.MAX_PAGE_SIZE}')
        return self


class MaskedBaseModel(BaseModel):
    allowed_fields: list[str] | None = Field(None)

    @model_validator(mode='after')
    def mask_fields(self):
        if self.allowed_fields is None:
            return self

        for field in self.__class__.model_fields.keys():
            if field == 'allowed_fields':
                continue
            if field not in self.allowed_fields:
                setattr(self, field, None)
        return self


class SimpleOrganizationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field()
    name: str


class SimpleDepartmentDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field()
    name: str


class SimpleLocationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field()
    name: str


class SimplePositionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field()
    title: str | None = Field()
