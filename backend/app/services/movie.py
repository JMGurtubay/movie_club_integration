from typing import List
from app.database.connection import db
from app.models.movie import MovieDB
from app.schemas.movie import MovieRequest
from pymongo.errors import PyMongoError
from bson import ObjectId

movies_collection = db["movies"]

def get_all_movies_service() -> List[MovieDB]:
    try:
        print('Entra al servicio')
        movies_cursor = movies_collection.find({})
        print('lista de peliculas')
        movies = [
            MovieDB(
                id=str(movie["_id"]),
                title=movie["title"],
                overview=movie["overview"],
                year=movie["year"],
                rating=movie["rating"],
                category=movie["category"],
                duration=movie["duration"]
            )
            for movie in movies_cursor
        ]
        return movies
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_movie_by_id_service(movie_id: str) -> MovieDB:
    try:
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            return None
        return MovieDB(
            id=str(movie["_id"]),
            title=movie["title"],
            overview=movie["overview"],
            year=movie["year"],
            rating=movie["rating"],
            category=movie["category"],
            duration=movie["duration"]
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_movie_service(movie_data: MovieRequest) -> MovieDB:
    try:
        result = movies_collection.insert_one(movie_data.model_dump(exclude={"id"}))

        created_movie = movies_collection.find_one({"_id": result.inserted_id})

        return MovieDB(
            id=str(created_movie["_id"]),
            title=created_movie["title"],
            overview=created_movie["overview"],
            year=created_movie["year"],
            rating=created_movie["rating"],
            category=created_movie["category"],
            duration=created_movie["duration"]
        )

    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")

def update_movie_service(movie_id: str, movie_data: MovieRequest) -> MovieDB:
    try:
        # Actualizar el documento en MongoDB
        result = movies_collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": movie_data.model_dump(exclude={"id"})}
        )

        # Verificar si se modificó algún documento
        if result.matched_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {movie_id}")

        # Obtener la película actualizada para regresarla como respuesta
        updated_movie = movies_collection.find_one({"_id": ObjectId(movie_id)})

        # Convertir el resultado a un objeto MovieDB
        return MovieDB(**updated_movie)
        
    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")

def delete_movie_service(movie_id: str) -> bool:
    try:

        # Intentar eliminar la película de la base de datos
        result = movies_collection.delete_one({"_id": ObjectId(movie_id)})

        # Verificar si se eliminó algún documento
        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {movie_id}")

        return True  # Indica que la película fue eliminada exitosamente

    except PyMongoError as e:
        print('Mongo')
        raise RuntimeError(f"Database error: {str(e)}")

