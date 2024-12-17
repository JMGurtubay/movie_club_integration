from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from app.services.like import (
    get_movie_likes,
    get_like_by_id_service,
    create_like_service,
    delete_like_service,
    delete_movie_likes_service
)
from app.schemas.like import LikeRequest, LikeResponse
from app.models.like import LikeDB
from app.shared.utils import validate_object_id

router = APIRouter()

@router.get("/movie/{movie_id}", response_model=LikeResponse)
def get_likes_by_movie(movie_id: str):
    """
    Obtiene todos los likes asociados a una película específica.

    Parámetros:
        - movie_id (str): ID de la película.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Lista de likes obtenidos.
    """
    try:
        validate_object_id(movie_id)
        likes = get_movie_likes(movie_id)
        return LikeResponse(
            code=200,
            message="Likes obtenidos con éxito.",
            description="Se obtuvieron correctamente los likes de la película.",
            data=likes
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )

@router.get("/{like_id}", response_model=LikeResponse)
def get_like(like_id: str):
    """
    Obtiene un like específico por su ID.

    Parámetros:
        - like_id (str): ID del like a buscar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Datos del like encontrado.
    """
    try:
        validate_object_id(like_id)
        like = get_like_by_id_service(like_id)
        if not like:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Like no encontrado.",
                    "description": "No se encontró un like con el ID proporcionado."
                }
            )
        return LikeResponse(
            code=200,
            message="Like obtenido con éxito.",
            description="Se obtuvo correctamente el like solicitado.",
            data=like
        )
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

@router.post("/", response_model=LikeResponse)
def create_like(like: LikeRequest):
    """
    Crea un nuevo like en la base de datos.

    Parámetros:
        - like (LikeRequest): Objeto con los datos del like a crear.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos del like creado.
    """
    try:
        created_like = create_like_service(like)
        return LikeResponse(
            code=200,
            message="Like creado exitosamente.",
            description="El like ha sido añadido correctamente a la base de datos.",
            data=created_like
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Error de validación.",
                "description": str(e)
            }
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )

@router.delete("/{like_id}", response_model=LikeResponse)
def delete_like(like_id: str):
    """
    Elimina un like de la base de datos por su ID.

    Parámetros:
        - like_id (str): ID del like a eliminar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Ninguno.
    """
    try:
        validate_object_id(like_id)
        delete_like_service(like_id)
        return LikeResponse(
            code=200,
            message="Like eliminado exitosamente.",
            description="Se eliminó correctamente el like de la base de datos.",
            data=None
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Like no encontrado.",
                "description": str(e)
            }
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )

@router.delete("/movie/{movie_id}", response_model=LikeResponse)
def delete_movie_likes(movie_id: str):
    """
    Elimina todos los likes asociados a una película.

    Parámetros:
        - movie_id (str): ID de la película cuyos likes se eliminarán.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Ninguno.
    """
    try:
        validate_object_id(movie_id)
        delete_movie_likes_service(movie_id)
        return LikeResponse(
            code=200,
            message="Likes eliminados exitosamente.",
            description="Se eliminaron correctamente todos los likes de la película.",
            data=None
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error en la base de datos.",
                "description": str(e)
            }
        )