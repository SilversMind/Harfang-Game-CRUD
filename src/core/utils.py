from src.core.models import Platform
from datetime import date

def validate_name(name):
    if not name:
        raise ValueError('Name should not be empty')
    return name


def convert_release_year_date(year_value):
    if year_value:
        return date(int(year_value), 1, 1)

def transform_platforms(platforms: list[str]) -> list[Platform]:
        return [Platform(name=platform) for platform in platforms]

def split_platforms(platforms: str) -> list[str]:
    return platforms.split(",") if platforms else []