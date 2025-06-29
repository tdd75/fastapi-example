from sqlalchemy import ColumnElement, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.model.mixin import TrackTimeMixin


class User(TrackTimeMixin, Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    phone: Mapped[str | None]

    @hybrid_property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @full_name.inplace.expression
    @classmethod
    def _full_name_expression(cls) -> ColumnElement[str]:
        return func.concat(cls.first_name, ' ', cls.last_name)




