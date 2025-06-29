import datetime
import typing

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.constant.employee_constant import EmployeeStatus
from app.db.base import Base
from app.model.mixin import TrackTimeMixin

if typing.TYPE_CHECKING:
    from app.model.department import Department
    from app.model.location import Location
    from app.model.organization import Organization
    from app.model.position import Position


class Employee(TrackTimeMixin, Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(Text, index=True)
    last_name: Mapped[str] = mapped_column(Text, index=True)
    email: Mapped[str] = mapped_column(Text, index=True)
    phone: Mapped[str] = mapped_column(Text, nullable=True)
    hire_date: Mapped[datetime.date] = mapped_column(DateTime(timezone=True))
    status: Mapped[EmployeeStatus] = mapped_column(Text, default='active', index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organization.id'))
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'))
    location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    position_id: Mapped[int] = mapped_column(ForeignKey('position.id'))
    manager_id: Mapped[int | None] = mapped_column(ForeignKey('employee.id'))

    # Relationships
    organization: Mapped['Organization'] = relationship('Organization', foreign_keys=[organization_id])
    department: Mapped['Department'] = relationship('Department', foreign_keys=[department_id])
    location: Mapped['Location'] = relationship('Location', foreign_keys=[location_id])
    position: Mapped['Position'] = relationship('Position', foreign_keys=[position_id])
    manager: Mapped['Employee'] = relationship('Employee', remote_side=[id], foreign_keys=[manager_id])

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
