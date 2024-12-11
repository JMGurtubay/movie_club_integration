from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional, Dict, Union
from app.models.theater import TheaterDB


class TheaterRequest(BaseModel):
    name: str
    max_capacity: int = Field(gt=0, description="Capacidad máxima de personas en la sala")
    projection: str = Field(description="Tamaño de la proyección (e.g., 1080p, 4K)")
    screen_size:str
    description: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Anfiteatro Griego",
                "max_capacity": 35,
                "projection": "4K",
                "screen_size": '120"',
                "description": "Sala ambientada en un anfiteatro griego con sonido envolvente",
            }
        }
    )



class TheaterResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Union[TheaterDB, Dict, List[TheaterDB]]] = None

