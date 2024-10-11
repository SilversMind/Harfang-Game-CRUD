from src.core.models import Game
from fastapi import HTTPException
from fastapi import Depends
from src.core.dependencies import get_db


def create_game(game: Game, db=Depends(get_db)):
    db_game = Game(
        name=game.name,
        release_date=game.release_date,
        studio=game.studio,
        ratings=game.ratings,
        platforms=game.platforms,
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def update_game(game_id: int, game: Game, db=Depends(get_db)):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.name is not None:
        db_game.name = game.name
    if game.release_date is not None:
        db_game.release_date = game.release_date
    if game.studio is not None:
        db_game.studio = game.studio
    if game.ratings is not None:
        db_game.ratings = game.ratings
    if game.platforms is not None:
        db_game.platforms = game.platforms


def delete_game(game_id: int, db=Depends(get_db)):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        return None
    db.delete(db_game)
    db.commit()
    return db_game


def get_games(
    db=Depends(get_db),
    name: str = None,
    release_date: str = None,
    studio: str = None,
    ratings: int = None,
):
    query = db.query(Game)

    if name:
        query = query.filter(Game.name == name)
    if release_date:
        query = query.filter(Game.release_date == release_date)
    if studio:
        query = query.filter(Game.studio == studio)
    if ratings:
        query = query.filter(Game.ratings == ratings)

    return query.all()
