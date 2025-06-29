import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class TrackTimeMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())
