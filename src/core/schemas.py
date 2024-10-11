from pydantic import BaseModel, Field, field_validator
from typing import Union
from src.core.utils import validate_name


class CreateGameSchema(BaseModel):
    name: str = Field(..., min_length=1, description="name must not be empty")
    release_date: str
    studio: str
    ratings: int = Field(..., ge=0, le=100)
    platforms: list[str]

    _validate_name = field_validator('name')(validate_name)

class UpdateGameSchema(BaseModel):
    id: int
    name: Union[str, None] = None
    release_date: Union[str, None] = None
    studio: Union[str, None] = None
    ratings: Union[int, None] = None
    platforms: Union[list[str], None] = None