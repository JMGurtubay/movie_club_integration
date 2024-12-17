from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict, Union
from app.models.comment import CommentDB

# Esquema para crear un comentario
class CommentRequest(BaseModel):
    user_id: str = Field(..., min_length=24, max_length=24, description="El ID del usuario debe tener 24 caracteres.")
    movie_id: str = Field(..., min_length=24, max_length=24, description="El ID de la película debe tener 24 caracteres.")
    parent_comment_id: Optional[str] = Field(None, min_length=24, max_length=24, description="El ID del comentario padre debe tener 24 caracteres.")
    comment_content: str = Field(..., min_length=1, max_length=500, description="El contenido del comentario no debe exceder los 500 caracteres.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "movie_id": "507f1f77bcf86cd799439012",
                "parent_comment_id": None,
                "comment_content": "¡Excelente película! La recomiendo totalmente."
            }
        }
    )

# Esquema para actualizar un comentario
class CommentUpdateRequest(BaseModel):
    comment_content: str = Field(..., min_length=1, max_length=500, description="El contenido del comentario no debe exceder los 500 caracteres.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "comment_content": "¡Excelente película! Definitivamente una obra maestra."
            }
        }
    )

# Esquema de respuesta del comentario
class CommentResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Union[CommentDB, Dict, List[CommentDB]]] = None
