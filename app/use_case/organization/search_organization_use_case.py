from sqlalchemy.orm import Session

from app.dto.organization_dto import OrganizationListDTO
from app.repository import organization_repository


def execute(
    session: Session,
    keyword: str | None,
    limit: int,
    offset: int,
) -> OrganizationListDTO:
    organizations, total = organization_repository.search(
        session,
        keyword=keyword,
        limit=limit,
        offset=offset,
    )
    return OrganizationListDTO(items=organizations, total=total)
