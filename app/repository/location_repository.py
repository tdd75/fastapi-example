from sqlalchemy.orm import Session

from app.model.location import Location


def search(
    session: Session,
    keyword: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> tuple[list[Location], int]:
    query = session.query(Location)

    # filter
    filters = []
    if keyword is not None:
        filters.append(Location.name.ilike('%' + keyword + '%'))

    query = query.filter(*filters)
    results = query.limit(limit).offset(offset).all()
    count = query.count()

    return results, count


def find_by_id(session: Session, location_id: int) -> Location | None:
    return session.query(Location).filter(Location.id == location_id).first()


def find_by_email(session: Session, email: str) -> Location | None:
    return session.query(Location).filter(Location.email == email).first()


def create(session: Session, location: Location) -> Location:
    session.add(location)
    session.flush([location])
    session.refresh(location)

    return location


def update(session: Session, location: Location) -> Location:
    session.flush([location])
    session.refresh(location)

    return location


def delete(session: Session, location: Location) -> None:
    session.delete(location)
    session.flush()
