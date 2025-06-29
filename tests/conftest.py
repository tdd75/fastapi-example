import pytest
from fastapi.testclient import TestClient
from typing import Generator

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session

from app import connection_pool
from app.db.base import Base
from app.main import app

connection_pool.engine = create_engine(
    'sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool
)
connection_pool.session_factory = scoped_session(
    sessionmaker(
        bind=connection_pool.engine, autocommit=False, autoflush=False, expire_on_commit=False
    )
)


@pytest.fixture(autouse=True)
def setup_test() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=connection_pool.engine)
    yield
    Base.metadata.drop_all(bind=connection_pool.engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app=app)
