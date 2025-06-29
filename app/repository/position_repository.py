from sqlalchemy.orm import Session

from app.model.position import Position


def search(
    session: Session,
    keyword: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> tuple[list[Position], int]:
    query = session.query(Position)

    # filter
    filters = []
    if keyword is not None:
        filters.append(Position.title.ilike('%' + keyword + '%'))

    query = query.filter(*filters)
    results = query.limit(limit).offset(offset).all()
    count = query.count()

    return results, count


def find_by_id(session: Session, position_id: int) -> Position | None:
    return session.query(Position).filter(Position.id == position_id).first()


def find_by_email(session: Session, email: str) -> Position | None:
    return session.query(Position).filter(Position.email == email).first()


def create(session: Session, position: Position) -> Position:
    session.add(position)
    session.flush([position])
    session.refresh(position)

    return position


def update(session: Session, position: Position) -> Position:
    session.flush([position])
    session.refresh(position)

    return position


def delete(session: Session, position: Position) -> None:
    session.delete(position)
    session.flush()
