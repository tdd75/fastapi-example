from sqlalchemy.orm import Session

from app.dto.department_dto import DepartmentListDTO
from app.repository import department_repository


def execute(
    session: Session,
    keyword: str | None,
    limit: int,
    offset: int,
) -> DepartmentListDTO:
    departments, total = department_repository.search(
        session,
        keyword=keyword,
        limit=limit,
        offset=offset,
    )
    return DepartmentListDTO(items=departments, total=total)
