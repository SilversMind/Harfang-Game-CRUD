from sqlalchemy.orm import Session
from src.core.crud import get_games, get_number_of_games_by_platform
from src.core.constants import GAMES_ON_DASHBOARD
from datetime import date


def get_dashboard(db: Session):
    date_today = date.today()
    top_games = get_games(
        db=db, limit=GAMES_ON_DASHBOARD, release_date=date_today, sort_by="ratings"
    )
    last_released_games = get_games(
        db=db, limit=GAMES_ON_DASHBOARD, release_date=date_today, sort_by="release_date"
    )
    number_of_games_by_platform = get_number_of_games_by_platform(db=db)
    return {
        "top-games": top_games,
        "last-released-games": last_released_games,
        "number-of-games-by-platform": number_of_games_by_platform,
    }
