import pytest
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.models import Base
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.core.router import game_router
from src.core.utils import transform_platforms
from src.core.dependencies import get_db
from src.core.models import Game, Platform, game_platforms
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
        db.execute(game_platforms.delete())
        db.query(Game).delete()
        db.query(Platform).delete()
        db.commit()

        with open(Path(__file__).parent / 'test_data/games.json') as f_in:
            games_data = json.load(f_in)
            for game_data in games_data:
                platforms = []
                for platform_name in game_data["platforms"]:
                    platform = db.query(Platform).filter_by(name=platform_name).first()
                    if not platform:
                        platform = Platform(name=platform_name)
                        db.add(platform)
                        db.commit()
                        db.refresh(platform)
                    platforms.append(platform)

                game = Game(
                    name=game_data["name"],
                    release_date=game_data["release_date"],
                    studio=game_data["studio"],
                    ratings=game_data["ratings"],
                    platforms=platforms
                )
                db.add(game)
            db.commit()
    finally:
        db.close()

    yield

    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    return client
