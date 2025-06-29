from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.dto.organization_dto import OrganizationListDTO, OrganizationQueryDTO
from app.use_case.organization import search_organization_use_case

organization_router = APIRouter(prefix='/organization', tags=['Organization'])


@organization_router.get('/')
def search_organizations(
    session: Annotated[Session, Depends(get_db)],
    query: Annotated[OrganizationQueryDTO, Query()],
) -> OrganizationListDTO:
    return search_organization_use_case.execute(
        session,
        keyword=query.keyword,
        limit=query.limit,
        offset=query.offset,
    )
