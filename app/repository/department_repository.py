from sqlalchemy.orm import Session

from app.model.department import Department


def search(
    session: Session,
    keyword: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> tuple[list[Department], int]:
    query = session.query(Department)

    # filter
    filters = []
    if keyword is not None:
        filters.append(Department.name.ilike('%' + keyword + '%'))

    query = query.filter(*filters)
    results = query.limit(limit).offset(offset).all()
    count = query.count()

    return results, count


def find_by_id(session: Session, department_id: int) -> Department | None:
    return session.query(Department).filter(Department.id == department_id).first()


def find_by_email(session: Session, email: str) -> Department | None:
    return session.query(Department).filter(Department.email == email).first()


def create(session: Session, department: Department) -> Department:
    session.add(department)
    session.flush([department])
    session.refresh(department)

    return department


def update(session: Session, department: Department) -> Department:
    session.flush([department])
    session.refresh(department)

    return department


def delete(session: Session, department: Department) -> None:
    session.delete(department)
    session.flush()
