from fastapi import APIRouter, HTTPException
from app.services.comment import (
    get_all_comments_service,
    get_comment_by_id_service,
    create_comment_service,
    update_comment_service,
    delete_comment_service
)
from app.schemas.comment import CommentRequest, CommentUpdateRequest, CommentResponse
from app.shared.utils import validate_object_id

router = APIRouter()

@router.get("/", response_model=CommentResponse)
def get_comments():
    """
    Obtiene la lista de todos los comentarios.

    Parámetros:
        - Ninguno.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Lista de comentarios obtenidos.
    """
    try:
        comments = get_all_comments_service()
        return CommentResponse(
            code=200,
            message="Comentarios obtenidos con éxito.",
            description="Se obtuvo correctamente la lista de comentarios.",
            data=comments
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: str):
    """
    Obtiene un comentario específico por su ID.

    Parámetros:
        - comment_id (str): ID del comentario a buscar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Datos del comentario encontrado.
    """
    try:
        validate_object_id(comment_id)
        comment = get_comment_by_id_service(comment_id)
        if not comment:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Comentario no encontrado.",
                    "description": "No se encontró un comentario con el ID proporcionado."
                }
            )
        return CommentResponse(
            code=200,
            message="Comentario obtenido con éxito.",
            description="Se obtuvo correctamente el comentario solicitado.",
            data=comment
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

@router.post("/", response_model=CommentResponse)
def create_comment(comment: CommentRequest):
    """
    Crea un nuevo comentario en la base de datos.

    Parámetros:
        - comment (CommentRequest): Objeto con los datos del comentario a crear.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos del comentario creado.
    """
    try:
        created_comment = create_comment_service(comment)
        return CommentResponse(
            code=200,
            message="El comentario ha sido creado exitosamente.",
            description="El comentario ha sido añadido correctamente a la base de datos.",
            data=created_comment
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: str, comment: CommentUpdateRequest):
    """
    Actualiza un comentario existente en la base de datos.

    Parámetros:
        - comment_id (str): ID del comentario a actualizar.
        - comment (CommentUpdateRequest): Objeto con el contenido actualizado del comentario.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos del comentario actualizado.
    """
    try:
        validate_object_id(comment_id)
        updated_comment = update_comment_service(comment_id, comment)
        return CommentResponse(
            code=200,
            message="El comentario ha sido actualizado exitosamente.",
            description="El contenido del comentario se ha modificado correctamente.",
            data=updated_comment
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

@router.delete("/{comment_id}", response_model=CommentResponse)
def delete_comment(comment_id: str):
    """
    Elimina un comentario de la base de datos por su ID.

    Parámetros:
        - comment_id (str): ID del comentario a eliminar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Ninguno.
    """
    try:
        validate_object_id(comment_id)
        delete_comment_service(comment_id)
        return CommentResponse(
            code=200,
            message="El comentario ha sido eliminado exitosamente.",
            description="Se eliminó correctamente el comentario de la base de datos.",
            data=None
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