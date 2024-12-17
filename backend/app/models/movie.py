from pydantic import BaseModel
from typing import List, Optional
from app.models.comment import CommentDB
from app.models.like import LikeDB

class MovieDB(BaseModel):
    id: str = None
    title: str
    overview: str
    year: int
    rating: float
    category: str
    duration: int
    comments: Optional[List[CommentDB]] = []
    likes: Optional[List[LikeDB]] = []
    likes_count: int = 0
    