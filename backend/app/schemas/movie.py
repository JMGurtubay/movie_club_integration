from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional, Dict, Union
from app.models.movie import MovieDB


class MovieRequest(BaseModel):

    title: str
    overview: str
    year: int
    rating: float
    category: str
    duration: int

    @field_validator("year")
    def validate_year(cls, value: int):
        current_year = datetime.now().year
        if value < 1900 or value > current_year:
            raise ValueError(f"El año debe estar entre 1900 y {current_year}.")
        return value
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
            "title": "Inception",
            "overview": "Es momento de entrar a los sueños para implentar una idea, este es el caso de ...",
            "year": 2010,
            "rating": 8.8,
            "category": "Sci-Fi",
            "duration": 148,
            }
        }
        
    )



class MovieResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Union[MovieDB, Dict, List[MovieDB]]] = None
