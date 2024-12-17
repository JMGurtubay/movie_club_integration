from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from app.services.movie import (
    get_all_movies_service, 
    get_movie_by_id_service, 
    create_movie_service, 
    update_movie_service, 
    delete_movie_service,
    get_movie_comments
)
from app.schemas.movie import MovieRequest, MovieResponse
from app.models.movie import MovieDB
from app.models.comment import CommentDB
from app.shared.utils import validate_object_id

router = APIRouter()

@router.get("/", response_model=MovieResponse)
def get_movies():
    """
    Obtiene la lista de todas las películas.

    Parámetros:
        - Ninguno.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Lista de películas obtenidas.
    """
    try:
        movies = get_all_movies_service()
        return MovieResponse(
            code=200,
            message="Películas obtenidas con éxito.",
            description="Se obtuvo correctamente la lista de películas.",
            data=movies
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: str):
    """
    Obtiene una película específica por su ID.

    Parámetros:
        - movie_id (str): ID de la película a buscar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Datos de la película encontrada.
    """
    try:
        validate_object_id(movie_id)  # Validar que el ID sea un ObjectId válido
        movie = get_movie_by_id_service(movie_id)
        if not movie:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Película no encontrada.",
                    "description": "No se encontró una película con el ID proporcionado."
                }
            )
        return MovieResponse(
            code=200,
            message="Película obtenida con éxito.",
            description="Se obtuvo correctamente la película solicitada.",
            data=movie
        )
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error inesperado en el servidor.",
                "description": str(e)
            }
        )


@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieRequest):
    """
    Crea una nueva película en la base de datos.

    Parámetros:
        - movie (MovieRequest): Objeto con los datos de la película a crear.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos de la película creada.
    """
    try:
        created_movie = create_movie_service(movie)
        return MovieResponse(
            code=200,
            message="La película ha sido creada exitosamente.",
            description="La película ha sido añadida correctamente a la base de datos.",
            data=created_movie
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: str, movie: MovieRequest):
    """
    Actualiza una película existente en la base de datos.

    Parámetros:
        - movie_id (str): ID de la película a actualizar.
        - movie (MovieRequest): Objeto con los datos actualizados de la película.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos de la película actualizada.
    """
    try:
        validate_object_id(movie_id)
        updated_movie = update_movie_service(movie_id, movie)
        return MovieResponse(
            code=200,
            message="La película ha sido actualizada exitosamente.",
            description="Los datos de la película se han modificado correctamente.",
            data=updated_movie
        )
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error inesperado en el servidor.",
                "description": str(e)
            }
        )


@router.delete("/{movie_id}", response_model=MovieResponse)
def delete_movie(movie_id: str):
    """
    Elimina una película de la base de datos por su ID.

    Parámetros:
        - movie_id (str): ID de la película a eliminar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Ninguno.
    """
    try:
        validate_object_id(movie_id)
        delete_movie_service(movie_id)
        return MovieResponse(
            code=200,
            message="La película ha sido eliminada exitosamente.",
            description="Se eliminó correctamente la película de la base de datos.",
            data=None
        )
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error inesperado en el servidor.",
                "description": str(e)
            }
        )

@router.get("/{movie_id}/comments", response_model=List[CommentDB])
def get_movie_comments_route(movie_id: str):
    """
    Obtiene todos los comentarios de una película específica.

    Parámetros:
        - movie_id (str): ID de la película.

    Respuesta:
        - Lista de comentarios asociados a la película.
    """
    try:
        validate_object_id(movie_id)
        # Verificar que la película existe
        movie = get_movie_by_id_service(movie_id)
        if not movie:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Película no encontrada.",
                    "description": "No se encontró una película con el ID proporcionado."
                }
            )
        
        comments = get_movie_comments(movie_id)
        return comments
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error inesperado en el servidor.",
                "description": str(e)
            }
        )