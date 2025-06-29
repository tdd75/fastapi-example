from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict

from app.constant.employee_constant import EmployeeStatus
from app.dto.common_dto import BaseQueryDTO, SimpleDepartmentDTO, SimpleOrganizationDTO, SimpleLocationDTO, \
    SimplePositionDTO, MaskedBaseModel


class EmployeeQueryDTO(BaseQueryDTO):
    organization_id: int = Query()
    keyword: str | None = Query(None, min_length=1, max_length=100)
    status: EmployeeStatus = Query(None)
    location_ids: list[int] = Query(None)
    organization_ids: list[int] = Query(None)
    department_ids: list[int] = Query(None)
    position_ids: list[int] = Query(None)


class EmployeeDTO(MaskedBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field()
    first_name: str | None = Field()
    last_name: str | None = Field()
    email: str | None = Field()
    phone: str | None = Field()
    organization: SimpleOrganizationDTO | None = Field()
    department: SimpleDepartmentDTO | None = Field()
    location: SimpleLocationDTO | None = Field()
    position: SimplePositionDTO | None = Field()
    status: EmployeeStatus | None = Field()


class EmployeeListDTO(BaseModel):
    items: list[EmployeeDTO] = Field()
    total: int = Field()
