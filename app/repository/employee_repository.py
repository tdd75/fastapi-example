from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, RelationshipProperty, class_mapper

from app.constant.employee_constant import EmployeeStatus, EmployeeAllowedFields
from app.helper.db_helper import is_scalar_field, is_relationship_field
from app.model.employee import Employee


def search(
    session: Session,
    keyword: str | None = None,
    fields: list[str] | None = None,
    status: EmployeeStatus | None = None,
    location_ids: list[int] | None = None,
    organization_ids: list[int] | None = None,
    department_ids: list[int] | None = None,
    position_ids: list[int] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> tuple[list[Employee], int]:
    query = session.query(Employee)

    if fields is not None:
        fields = [field for field in fields if field in EmployeeAllowedFields]

    # eager loading based on fields
    relationship_fields = [
        field
        for field in fields
        if is_relationship_field(Employee, field)
    ]
    if relationship_fields is not None:
        query = query.options(*(joinedload(getattr(Employee, field)) for field in relationship_fields))

    # join
    if location_ids is not None:
        query = query.join(Employee.location)
    if organization_ids is not None:
        query = query.join(Employee.organization)
    if department_ids is not None:
        query = query.join(Employee.department)
    if position_ids is not None:
        query = query.join(Employee.position)

    # filter
    filters = []
    if keyword is not None:
        keyword = f'%{keyword}%'
        filters.append(or_(
            Employee.first_name.ilike(keyword),
            Employee.last_name.ilike(keyword),
            Employee.email.ilike(keyword),
            Employee.phone.ilike(keyword),
        ))
    if status is not None:
        filters.append(Employee.status == status)
    if location_ids is not None:
        filters.append(Employee.location_id.in_(location_ids))
    if organization_ids is not None:
        filters.append(Employee.organization_id.in_(organization_ids))
    if department_ids is not None:
        filters.append(Employee.department_id.in_(department_ids))

    query = query.filter(*filters)
    results = query.limit(limit).offset(offset).all()
    count = query.count()

    return results, count


def find_by_id(session: Session, employee_id: int) -> Employee | None:
    return session.query(Employee).filter(Employee.id == employee_id).first()


def find_by_email(session: Session, email: str) -> Employee | None:
    return session.query(Employee).filter(Employee.email == email).first()


def create(session: Session, employee: Employee) -> Employee:
    session.add(employee)
    session.flush([employee])
    session.refresh(employee)

    return employee


def update(session: Session, employee: Employee) -> Employee:
    session.flush([employee])
    session.refresh(employee)

    return employee


def delete(session: Session, employee: Employee) -> None:
    session.delete(employee)
    session.flush()
