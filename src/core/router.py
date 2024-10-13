from fastapi import APIRouter, Depends
from src.core.dependencies import get_db
from src.core.models import Game
from src.core.schemas import CreateGameSchema, UpdateGameSchema, GetGameSchema
from src.core.crud import create_game, update_game, delete_game, get_games
from src.core.service import get_dashboard

game_router = APIRouter()

@game_router.get("/")
def get_games_endpoint(
    db=Depends(get_db),
    query_params: GetGameSchema = Depends()
):
    return get_games(
        db=db,
        name=query_params.name,
        release_date=query_params.release_date,
        studio=query_params.studio,
        ratings=query_params.ratings,
        platforms=query_params.platforms,
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

@game_router.get("/dashboard")
def get_dashboard_endpoint(db = Depends(get_db)):
    return get_dashboard(db=db)