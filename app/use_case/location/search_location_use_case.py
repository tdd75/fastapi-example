from sqlalchemy.orm import Session

from app.dto.location_dto import LocationListDTO
from app.repository import location_repository


def execute(
    session: Session,
    keyword: str | None,
    limit: int,
    offset: int,
) -> LocationListDTO:
    locations, total = location_repository.search(
        session,
        keyword=keyword,
        limit=limit,
        offset=offset,
    )
    return LocationListDTO(items=locations, total=total)
