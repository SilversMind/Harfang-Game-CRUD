import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.models import Base
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.core.router import game_router
from src.core.dependencies import get_db
from src.core.models import Game
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
app.include_router(game_router, prefix="/games")

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
        game1 = Game(
            name="The Witcher 3 : Wild Hunt",
            release_date="2015-05-19",
            studio="CD Projekt RED",
            ratings=19,
            platforms=["PC, PS4, PS5, Switch, One"]
        )
        game2 = Game(
            name="Mario Kart 8 Deluxe",
            release_date="2017-04-28",
            studio="Nintendo",
            ratings=17,
            platforms=["Switch"]
        )
        game3 = Game(
            name="Don't Starve",
            release_date="2013-04-23",
            studio="Capybara Games",
            ratings=17,
            platforms=["PC", "PS4", "Switch", "One", "WiiU", "PS3"]
        )
        db.add(game1)
        db.add(game2)
        db.add(game3)

        db.commit()
    finally:
        db.close()

    yield

    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    return client
