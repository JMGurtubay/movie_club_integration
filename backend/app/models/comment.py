from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CommentDB(BaseModel):
    id: str = None
    user_id: str
    movie_id: str
    parent_comment_id: Optional[str] = None
    comment_content: str
    created_at: datetime
    updated_at: Optional[datetime] = None