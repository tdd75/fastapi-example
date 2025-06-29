from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.dto.location_dto import LocationListDTO, LocationQueryDTO
from app.use_case.location import search_location_use_case

location_router = APIRouter(prefix='/location', tags=['Location'])


@location_router.get('/')
def search_locations(
    session: Annotated[Session, Depends(get_db)],
    query: Annotated[LocationQueryDTO, Query()],
) -> LocationListDTO:
    return search_location_use_case.execute(
        session,
        keyword=query.keyword,
        limit=query.limit,
        offset=query.offset,
    )
