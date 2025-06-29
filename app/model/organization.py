import typing

from sqlalchemy import Text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSON

from app.constant.employee_constant import EmployeeAllowedFields
from app.db.base import Base
from app.model.mixin import TrackTimeMixin

if typing.TYPE_CHECKING:
    from app.model.department import Department
    from app.model.employee import Employee
    from app.model.location import Location
    from app.model.position import Position


class Organization(TrackTimeMixin, Base):
    __tablename__ = 'organization'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text)
    domain: Mapped[str] = mapped_column(Text, unique=True, index=True)
    column_config: Mapped[JSON] = mapped_column(JSON, default=[field for field in EmployeeAllowedFields])

    # Relationships
    departments: Mapped[list['Department']] = relationship('Department', back_populates='organization')
    locations: Mapped[list['Location']] = relationship('Location', back_populates='organization')
    positions: Mapped[list['Position']] = relationship('Position', back_populates='organization')
    employees: Mapped[list['Employee']] = relationship('Employee', back_populates='organization')
