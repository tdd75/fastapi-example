from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.dto.position_dto import PositionListDTO, PositionQueryDTO
from app.use_case.position import search_position_use_case

position_router = APIRouter(prefix='/position', tags=['Position'])


@position_router.get('/')
def search_positions(
    session: Annotated[Session, Depends(get_db)],
    query: Annotated[PositionQueryDTO, Query()],
) -> PositionListDTO:
    return search_position_use_case.execute(
        session,
        keyword=query.keyword,
        limit=query.limit,
        offset=query.offset,
    )
