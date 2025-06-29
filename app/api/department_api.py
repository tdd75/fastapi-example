from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.dto.department_dto import DepartmentListDTO, DepartmentQueryDTO
from app.use_case.department import search_department_use_case

department_router = APIRouter(prefix='/department', tags=['Department'])


@department_router.get('/')
def search_departments(
    session: Annotated[Session, Depends(get_db)],
    query: Annotated[DepartmentQueryDTO, Query()],
) -> DepartmentListDTO:
    return search_department_use_case.execute(
        session,
        keyword=query.keyword,
        limit=query.limit,
        offset=query.offset,
    )
