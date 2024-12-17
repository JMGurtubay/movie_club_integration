from typing import List
from app.database.connection import db
from app.models.movie import MovieDB
from app.models.comment import CommentDB
from app.schemas.movie import MovieRequest
from pymongo.errors import PyMongoError
from bson import ObjectId
from app.services.like import get_movie_likes, delete_movie_likes_service

movies_collection = db["movies"]
comments_collection = db["comments"]

def update_movie_likes_count(movie_id: str) -> int:
    """Actualiza y retorna el contador de likes de una película"""
    try:
        likes = get_movie_likes(movie_id)
        likes_count = len(likes)
        
        # Actualizar el contador en la base de datos
        movies_collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": {"likes_count": likes_count}}
        )
        
        return likes_count
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_movie_comments(movie_id: str) -> List[CommentDB]:
    """Obtiene todos los comentarios asociados a una película."""
    try:
        comments_cursor = comments_collection.find({"movie_id": movie_id})
        return [
            CommentDB(
                id=str(comment["_id"]),
                user_id=comment["user_id"],
                movie_id=comment["movie_id"],
                parent_comment_id=comment.get("parent_comment_id"),
                comment_content=comment["comment_content"],
                created_at=comment["created_at"],
                updated_at=comment.get("updated_at")
            )
            for comment in comments_cursor
        ]
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_all_movies_service() -> List[MovieDB]:
    try:
        movies_cursor = movies_collection.find({})
        movies = []
        for movie in movies_cursor:
            comments = get_movie_comments(str(movie["_id"]))
            likes = get_movie_likes(str(movie["_id"]))
            likes_count = len(likes)
            movies.append(
                MovieDB(
                    id=str(movie["_id"]),
                    title=movie["title"],
                    overview=movie["overview"],
                    year=movie["year"],
                    rating=movie["rating"],
                    category=movie["category"],
                    duration=movie["duration"],
                    comments=comments,
                    likes=likes,
                    likes_count=likes_count
                )
            )
        return movies
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_movie_by_id_service(movie_id: str) -> MovieDB:
    try:
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            return None
            
        comments = get_movie_comments(movie_id)
        likes = get_movie_likes(movie_id)
        likes_count = len(likes)
        
        return MovieDB(
            id=str(movie["_id"]),
            title=movie["title"],
            overview=movie["overview"],
            year=movie["year"],
            rating=movie["rating"],
            category=movie["category"],
            duration=movie["duration"],
            comments=comments,
            likes=likes,
            likes_count=likes_count
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_movie_service(movie_data: MovieRequest) -> MovieDB:
    try:
        movie_dict = movie_data.model_dump(exclude={"id"})
        movie_dict["likes_count"] = 0  # Inicializar el contador de likes
        
        result = movies_collection.insert_one(movie_dict)
        created_movie = movies_collection.find_one({"_id": result.inserted_id})
        
        return MovieDB(
            id=str(created_movie["_id"]),
            title=created_movie["title"],
            overview=created_movie["overview"],
            year=created_movie["year"],
            rating=created_movie["rating"],
            category=created_movie["category"],
            duration=created_movie["duration"],
            comments=[],
            likes=[],
            likes_count=0
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def update_movie_service(movie_id: str, movie_data: MovieRequest) -> MovieDB:
    try:
        result = movies_collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": movie_data.model_dump(exclude={"id"})}
        )

        if result.matched_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {movie_id}")

        # Obtener la película actualizada con sus comentarios y likes
        updated_movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        comments = get_movie_comments(movie_id)
        likes = get_movie_likes(movie_id)
        likes_count = len(likes)
        
        return MovieDB(
            id=str(updated_movie["_id"]),
            title=updated_movie["title"],
            overview=updated_movie["overview"],
            year=updated_movie["year"],
            rating=updated_movie["rating"],
            category=updated_movie["category"],
            duration=updated_movie["duration"],
            comments=comments,
            likes=likes,
            likes_count=likes_count
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def delete_movie_service(movie_id: str) -> bool:
    try:
        # Eliminar la película
        result = movies_collection.delete_one({"_id": ObjectId(movie_id)})
        
        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {movie_id}")
        
        # Eliminar todos los comentarios asociados a la película
        comments_collection.delete_many({"movie_id": movie_id})
        
        # Eliminar todos los likes asociados a la película
        delete_movie_likes_service(movie_id)
        
        return True
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")