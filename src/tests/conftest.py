import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.models import Base
from src.core.models import Foo, Bar
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.core.router import router
from src.core.dependencies import get_db
from src.constants import MYSQL_TEST_DATABASE, MYSQL_PASSWORD, MYSQL_USER, MYSQL_HOST, MYSQL_PORT, MYSQL_ROOT_PASSWORD

initial_engine = create_engine(f"mysql+mysqlconnector://root:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}")
connection = initial_engine.connect()
connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_TEST_DATABASE}"))
connection.execute(text(f"GRANT ALL PRIVILEGES ON {MYSQL_TEST_DATABASE}.* TO '{MYSQL_USER}'@'%';"))
connection.close()

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_TEST_DATABASE}"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    # Insert mock data
    db = TestingSessionLocal()
    try:
        # Create mock authors
        foo1 = Foo(name="foo1")
        db.add(foo1)
        db.commit()
    finally:
        db.close()

    yield

    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    return client
