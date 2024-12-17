from pydantic import BaseModel
from datetime import datetime

class LikeDB(BaseModel):
    id: str = None
    user_id: str
    movie_id: str
    created_at: datetime = datetime.now()
    