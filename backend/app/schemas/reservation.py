# schemas/reservation.py
from pydantic import BaseModel, ConfigDict, Field, field_validator, validator
from bson import ObjectId
from collections import OrderedDict
from typing import List, Optional, Dict, Union
from datetime import datetime
from app.models.reservation import ReservationDB
from app.shared.utils import validate_object_id


class ReservationRequest(BaseModel):
    user_id: Optional[str] = Field(default=None)
    theater_id: str
    movie_id: str
    is_private: bool
    start_time: datetime 
    end_time: datetime 
    reservation_date: datetime 
    status: Optional[str] = "active"

    def validate_fields(self):
        # Validar los IDs usando la función validate_object_id
        self.theater_id = validate_object_id(self.theater_id)
        self.movie_id = validate_object_id(self.movie_id)
        self.user_id = validate_object_id(self.user_id)

    # Validadores para aceptar formatos legibles
    @field_validator("start_time", "end_time", mode="before")
    def parse_time(cls, value: str):
        try:
            return datetime.strptime(f"1970-01-01 {value}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError(f"Invalid time format. Use 'HH:mm'. Received: {value}")

    @field_validator("reservation_date", mode="before")
    def parse_date(cls, value: str):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format. Use 'YYYY-MM-DD'. Received: {value}")


    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()  # Serializar/formatear como ISO 8601
        },
        json_schema_extra={
            "example": OrderedDict(
                theater_id="64f1a4b2e3c9a5508d1e82e4",
                movie_id="64f1a4b2e3c9a5508d1e82e5",
                is_private=True,
                start_time="14:00",
                end_time="16:00",
                reservation_date="2024-11-26",
                status="active",
            )
        }
    )

class ReservationResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Union[ReservationDB, Dict, List[ReservationDB]]] = None

    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}
