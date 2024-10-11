from fastapi.testclient import TestClient

from conftest import app

client = TestClient(app)

def test_get_games():
    response = client.get("/games")
    assert response.status_code == 200

    # Test get_games without filters
    games_response = client.get("/games")
    games = games_response.json()
    assert len(games) == 3

    # Test get_games with name filter
    games_response = client.get("/games", params={"name": "The Witcher 3 : Wild Hunt"})
    games = games_response.json()
    assert len(games) == 1
    assert games[0]['name'] == "The Witcher 3 : Wild Hunt"

    # Test get_games with release_date filter
    games_response = client.get("/games", params={"release_date": "2017-04-28"})
    games = games_response.json()
    assert len(games) == 1
    assert games[0]['release_date'] == "2017-04-28"

    # Test get_games with studio filter
    games_response = client.get("/games", params={"studio": "Nintendo"})
    games = games_response.json()
    assert len(games) == 1
    assert games[0]['studio'] == "Nintendo"

    # Test get_games with ratings filter
    games_response = client.get("/games", params={"ratings": 17})
    games = games_response.json()
    assert len(games) == 2
    assert games[0]['ratings'] == 17