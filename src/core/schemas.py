from pydantic import BaseModel, Field, field_validator
from typing import Union, Optional, Annotated

from src.core.utils import validate_name, transform_platforms, split_platforms, convert_release_year_date


class GetGameSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    release_date: Optional[Annotated[int, Field(gt=1950, lt=2050)]] = None
    studio: Optional[str] = Field(None, min_length=1, max_length=100)
    ratings: Optional[Annotated[int, Field(gt=0, lt=20)]] = None
    platforms: Optional[str] = None

    validate_platforms = field_validator('platforms')(split_platforms)
    validate_date = field_validator('release_date')(convert_release_year_date)
    


class CreateGameSchema(BaseModel):
    name: str = Field(..., min_length=1, description="name must not be empty")
    release_date: str
    studio: str
    ratings: int = Field(..., ge=0, le=100)
    platforms: list[str]

    _validate_name = field_validator('name')(validate_name)
    validate_platforms = field_validator('platforms')(transform_platforms)


class UpdateGameSchema(BaseModel):
    id: int
    name: Union[str, None] = None
    release_date: Union[str, None] = None
    studio: Union[str, None] = None
    ratings: Union[int, None] = None
    platforms: Union[list[str], None] = None

    