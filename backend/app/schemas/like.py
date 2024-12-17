from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Union
from app.models.like import LikeDB

class LikeRequest(BaseModel):
    user_id: str
    movie_id: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "movie_id": "507f1f77bcf86cd799439012"
            }
        }
    )

class LikeResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Union[LikeDB, Dict, List[LikeDB]]] = None