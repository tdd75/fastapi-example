from sqlalchemy.orm import Session

from app.dto.position_dto import PositionListDTO
from app.repository import position_repository


def execute(
    session: Session,
    keyword: str | None,
    limit: int,
    offset: int,
) -> PositionListDTO:
    positions, total = position_repository.search(
        session,
        keyword=keyword,
        limit=limit,
        offset=offset,
    )
    return PositionListDTO(items=positions, total=total)
