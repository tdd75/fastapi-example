import logging
from typing import Generator

from sqlalchemy.orm import Session

from app import connection_pool

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    with connection_pool.open_session() as session:
        yield session
