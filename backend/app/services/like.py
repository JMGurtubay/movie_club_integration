from typing import List
from datetime import datetime
from app.database.connection import db
from app.models.like import LikeDB
from app.schemas.like import LikeRequest
from pymongo.errors import PyMongoError
from bson import ObjectId

likes_collection = db["likes"]

def get_movie_likes(movie_id: str) -> List[LikeDB]:
    """Obtiene todos los likes asociados a una película."""
    try:
        likes_cursor = likes_collection.find({"movie_id": movie_id})
        return [
            LikeDB(
                id=str(like["_id"]),
                user_id=like["user_id"],
                movie_id=like["movie_id"],
                created_at=like["created_at"]
            )
            for like in likes_cursor
        ]
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_like_by_id_service(like_id: str) -> LikeDB:
    try:
        like = likes_collection.find_one({"_id": ObjectId(like_id)})
        if not like:
            return None
        
        return LikeDB(
            id=str(like["_id"]),
            user_id=like["user_id"],
            movie_id=like["movie_id"],
            created_at=like["created_at"]
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_like_service(like_data: LikeRequest) -> LikeDB:
    try:
        # Verificar si ya existe un like del mismo usuario para la misma película
        existing_like = likes_collection.find_one({
            "user_id": like_data.user_id,
            "movie_id": like_data.movie_id
        })
        
        if existing_like:
            raise ValueError("El usuario ya dio like a esta película")
            
        like_dict = like_data.model_dump()
        like_dict["created_at"] = datetime.now()
        
        result = likes_collection.insert_one(like_dict)
        created_like = likes_collection.find_one({"_id": result.inserted_id})
        
        # Actualizar el contador de likes en la película
        from app.services.movie import update_movie_likes_count
        update_movie_likes_count(like_data.movie_id)
        
        return LikeDB(
            id=str(created_like["_id"]),
            user_id=created_like["user_id"],
            movie_id=created_like["movie_id"],
            created_at=created_like["created_at"]
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def delete_like_service(like_id: str) -> bool:
    try:
        # Obtener el like antes de eliminarlo para tener el movie_id
        like = likes_collection.find_one({"_id": ObjectId(like_id)})
        if not like:
            raise ValueError(f"No se encontró ningún like con el ID proporcionado: {like_id}")
        
        movie_id = like["movie_id"]
        
        # Eliminar el like
        result = likes_collection.delete_one({"_id": ObjectId(like_id)})
        
        # Actualizar el contador de likes en la película
        update_movie_likes_count(movie_id)
        
        return True
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    
def delete_movie_likes_service(movie_id: str) -> bool:
    """Elimina todos los likes asociados a una película."""
    try:
        result = likes_collection.delete_many({"movie_id": movie_id})
        return True
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")