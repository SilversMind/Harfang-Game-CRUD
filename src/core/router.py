from fastapi import APIRouter, Depends
from src.core.dependencies import get_db
from src.core.models import Game
from src.core.schemas import CreateGameSchema, UpdateGameSchema
from src.core.crud import create_game, update_game, delete_game, get_games
from typing import Optional

game_router = APIRouter()


@game_router.get("/")
def get_games_endpoint(
    db=Depends(get_db),
    name: Optional[str] = None,
    release_date: Optional[str] = None,
    studio: Optional[str] = None,
    ratings: Optional[int] = None,
):
    return get_games(
        db=db, name=name, release_date=release_date, studio=studio, ratings=ratings
    )


@game_router.post("/")
def create_game_endpoint(game: CreateGameSchema, db=Depends(get_db)):
    game = Game(
        name=game.name,
        release_date=game.release_date,
        studio=game.studio,
        ratings=game.ratings,
        platforms=game.platforms,
    )
    return create_game(game=game, db=db)


@game_router.put("/{game_id}")
def update_game_endpoint(game: UpdateGameSchema, db=Depends(get_db)):
    return update_game(game_id=game.id, game=game, db=db)


@game_router.delete("/{game_id}")
def delete_game_endpoint(game_id: int, db=Depends(get_db)):
    return delete_game(game_id=game_id, db=db)
