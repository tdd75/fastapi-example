from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.core.rate_limiter import rate_limit_decorator, get_ip_identifier, SEARCH_RATE_LIMITER
from app.dto.employee_dto import EmployeeListDTO, EmployeeQueryDTO
from app.use_case.employee import search_employee_use_case

employee_router = APIRouter(prefix='/employee', tags=['Employee'])


@employee_router.get('/')
@rate_limit_decorator(SEARCH_RATE_LIMITER, get_ip_identifier)
def search_employees(
    request: Request,
    session: Annotated[Session, Depends(get_db)],
    query: Annotated[EmployeeQueryDTO, Query()],
) -> EmployeeListDTO:
    return search_employee_use_case.execute(
        session,
        keyword=query.keyword,
        status=query.status,
        # TODO: Get organization_id from user context/JWT token instead of query parameter
        organization_id=query.organization_id,
        location_ids=query.location_ids,
        organization_ids=query.organization_ids,
        department_ids=query.department_ids,
        position_ids=query.position_ids,
        limit=query.limit,
        offset=query.offset,
    )
