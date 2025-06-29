import typing

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.db.base import Base
from app.model.mixin import TrackTimeMixin

if typing.TYPE_CHECKING:
    from app.model.employee import Employee
    from app.model.organization import Organization


class Position(TrackTimeMixin, Base):
    __tablename__ = 'position'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    level: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organization.id'))

    # Relationships
    organization: Mapped['Organization'] = relationship('Organization', foreign_keys=[organization_id])
    employees: Mapped[list['Employee']] = relationship('Employee', back_populates='position')
