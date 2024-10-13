from src.core.models import Game, Platform
from fastapi import HTTPException
from fastapi import Depends
from src.core.dependencies import get_db
from sqlalchemy.orm import joinedload
from sqlalchemy import desc, extract, func
from fuzzywuzzy import fuzz
import logging
from src.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

def create_game(game: Game, db=Depends(get_db)):
    try:
        existing_games = db.query(Game.name).all()
        existing_game_names = [g.name for g in existing_games]

        for existing_name in existing_game_names:
            similarity_score = fuzz.ratio(game.name, existing_name)
            if similarity_score > 90:
                raise HTTPException(status_code=409, detail=f"Game name '{game.name}' is too similar to existing game '{existing_name}'")
        platforms = []
        for platform in game.platforms:
            query_platform = db.query(Platform).filter(Platform.name==platform.name).first()
            if not query_platform:
                new_platform = Platform(name=platform.name)
                db.add(new_platform)
                db.commit()
                db.refresh(new_platform)
                platforms.append(new_platform)
            else:
                platforms.append(query_platform)

        game.platforms = platforms
        db.add(game)
        db.commit()
        db.refresh(game)
        return game
    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise exc
        db.rollback()
        logger.error(f"An unexpected error occurred: {exc}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")



def update_game(game_id: int, game: Game, db=Depends(get_db)):
    try:
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
        db.commit()
        db.refresh(db_game)
        
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


def delete_game(game_id: int, db=Depends(get_db)):
    try:
        db_game = db.query(Game).filter(Game.id == game_id).first()
        if not db_game:
            return HTTPException(status_code=404, detail="Game not found")
        db.delete(db_game)
        db.commit()
        return db_game
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


def get_games(
    db=Depends(get_db),
    name: str = None,
    release_date: str = None,
    studio: str = None,
    ratings: int = None,
    platforms: list[str] = None,
    limit: int = None,
    sort_by: str = None,
):
    query = db.query(Game).options(joinedload(Game.platforms))

    if name:
        query = query.filter(Game.name == name)
    if release_date:
        query = query.filter(extract('year', Game.release_date) == release_date.year)
    if studio:
        query = query.filter(Game.studio == studio)
    if ratings:
        query = query.filter(Game.ratings == ratings)
    if platforms:
        query = query.join(Game.platforms).filter(Platform.name.in_(platforms))
    
    if sort_by:
        query = query.order_by(desc(getattr(Game, sort_by)))

    if limit:
        query = query.limit(limit)
    
    result = []
    for game in query.all():
        result.append({
            "name": game.name,
            "release_date": game.release_date,
            "studio": game.studio,
            "ratings": game.ratings,
            "platforms": [platform.name for platform in game.platforms] 
        })

    return result

def get_number_of_games_by_platform(db=Depends(get_db)):
    result = db.query(Platform.name, func.count(Game.id).label('game_count')) \
               .join(Game.platforms) \
               .group_by(Platform.name) \
               .all()
    
    return [{"platform": row[0], "game_count": row[1]} for row in result]
    