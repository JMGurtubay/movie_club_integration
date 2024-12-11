from pydantic import BaseModel, Field
from datetime import datetime

class ReservationDB(BaseModel):
    id: str = None
    user_id: str
    theater_id: str
    movie_id: str
    is_private: bool
    start_time: datetime
    end_time: datetime
    reservation_date: datetime
    status: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%H:%M") if v.time() else v.strftime("%Y-%m-%d")
        }
    


