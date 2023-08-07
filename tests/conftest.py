import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from apps.admin import routes as admin_routes

from core.config import app_settings
from core.database import Base

engine: Engine = create_engine(app_settings.TESTING_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(admin_routes.router)
    return app


@pytest.fixture(scope="function")
def app():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Base.metadata.bind = engine
    TestingSessionLocal.bind = engine
    app = start_application()
    yield app


@pytest.fixture(scope="function", autouse=True)
def db(app):
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db  # use the session in tests.
    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app):
    client = TestClient(app)
    yield client
