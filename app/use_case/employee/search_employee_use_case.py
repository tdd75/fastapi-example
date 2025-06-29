from sqlalchemy.orm import Session

from app.constant.employee_constant import EmployeeStatus
from app.dto.employee_dto import EmployeeListDTO, EmployeeDTO
from app.repository import employee_repository, organization_repository


def execute(
    session: Session,
    organization_id: int,
    keyword: str | None,
    status: EmployeeStatus | None,
    location_ids: list[int] | None,
    organization_ids: list[int] | None,
    department_ids: list[int] | None,
    position_ids: list[int] | None,
    limit: int,
    offset: int,
) -> EmployeeListDTO:
    organization = organization_repository.find_by_id(session, organization_id)
    allowed_fields: list[str] = list(set(organization.column_config) | {'id'})
    employees, total = employee_repository.search(
        session,
        keyword=keyword,
        fields=allowed_fields,
        status=status,
        location_ids=location_ids,
        organization_ids=organization_ids,
        department_ids=department_ids,
        position_ids=position_ids,
        limit=limit,
        offset=offset,
    )

    items = []
    for e in employees:
        dto = EmployeeDTO.model_validate(e)
        dto.allowed_fields = allowed_fields
        items.append(dto)

    return EmployeeListDTO(items=items, total=total)
