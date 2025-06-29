from sqlalchemy.orm import Session

from app.model.organization import Organization


def search(
    session: Session,
    keyword: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> tuple[list[Organization], int]:
    query = session.query(Organization)

    # filter
    filters = []
    if keyword is not None:
        filters.append(Organization.name.ilike('%' + keyword + '%'))

    query = query.filter(*filters)
    results = query.limit(limit).offset(offset).all()
    count = query.count()

    return results, count


def find_by_id(session: Session, organization_id: int) -> Organization | None:
    return session.query(Organization).filter(Organization.id == organization_id).first()


def find_by_email(session: Session, email: str) -> Organization | None:
    return session.query(Organization).filter(Organization.email == email).first()


def create(session: Session, organization: Organization) -> Organization:
    session.add(organization)
    session.flush([organization])
    session.refresh(organization)

    return organization


def update(session: Session, organization: Organization) -> Organization:
    session.flush([organization])
    session.refresh(organization)

    return organization


def delete(session: Session, organization: Organization) -> None:
    session.delete(organization)
    session.flush()
