from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from conftest import app
from copy import deepcopy

client = TestClient(app)

game = {
    "name": "The Witcher 3 : Wild Hunt",
    "release_date": "2015-05-19",
    "studio": "CD Projekt RED",
    "ratings": 19,
    "platforms": ["PC", "PS4", "PS5", "Switch", "One"],
}


@pytest.fixture
def game0():
    return deepcopy(game)


def test_get_games():
    response = client.get("/games")
    assert response.status_code == 200

    # Test get_games without filters
    games_response = client.get("/games")
    games = games_response.json()
    assert len(games) == 28

    # Test get_games with name filter
    games_response = client.get("/games", params={"name": "The Witcher 3 : Wild Hunt"})
    games = games_response.json()
    assert len(games) == 1
    assert games[0]["name"] == "The Witcher 3 : Wild Hunt"

    # Test get_games with release_date filter
    games_response = client.get("/games", params={"release_date": "2021"})
    games = games_response.json()
    assert len(games) == 7
    assert all(game["release_date"].startswith("2021") for game in games)

    # Test get_games with studio filter
    games_response = client.get("/games", params={"studio": "CD Projekt RED"})
    games = games_response.json()
    assert len(games) == 2
    assert all(game["studio"] == "CD Projekt RED" for game in games)

    # Test get_games with ratings filter
    games_response = client.get("/games", params={"ratings": 17})
    games = games_response.json()
    assert len(games) == 5
    assert all(game["ratings"] == 17 for game in games)


def test_dashboard():
    response = client.get("/games/dashboard")
    assert response.status_code == 200

    dashboard = response.json()
    assert len(dashboard["top-games"]) == 3
    assert len(dashboard["last-released-games"]) == 3
    ps4_game_count = next(
        (
            item["game_count"]
            for item in dashboard["number-of-games-by-platform"]
            if item["platform"] == "PS4"
        ),
        None,
    )
    assert ps4_game_count == 15


def test_similar_games(game0):
    game0["name"] = "The Snitcher 3 : Wild Hunt"
    response = client.post("/games/", json=game0)
    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "Game name 'The Snitcher 3 : Wild Hunt' is too similar to existing game 'The Witcher 3 : Wild Hunt'"
    )
