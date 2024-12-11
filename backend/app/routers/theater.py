from fastapi import APIRouter, HTTPException
from app.services.theater import get_all_theaters_service, get_theater_by_id_service, create_theater_service, update_theater_service, delete_theater_service
from app.schemas.theater import TheaterRequest, TheaterResponse
from app.shared.utils import validate_object_id

router = APIRouter()

@router.get("/", response_model=TheaterResponse)
def get_theaters():
    """
    Obtiene la lista de todas las salas de proyección.

    Parámetros:
        - Ninguno.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Lista de salas de proyección obtenidas.
    """
    try:
        theaters = get_all_theaters_service()
        return TheaterResponse(
            code=200,
            message="Salas de proyección obtenidas con éxito.",
            description="Se obtuvo correctamente la lista de salas de proyección.",
            data=theaters
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{theater_id}", response_model=TheaterResponse)
def get_theater(theater_id: str):
    """
    Obtiene una sala de proyección específica por su ID.

    Parámetros:
        - theater_id (str): ID de la sala de proyección a buscar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Datos de la sala de proyección encontrada.
    """
    try:
        validate_object_id(theater_id)
        theater = get_theater_by_id_service(theater_id)
        if not theater:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Sala de proyección no encontrada.",
                    "description": "No se encontró una sala de proyección con el ID proporcionado."
                }
            )
        return TheaterResponse(
            code=200,
            message="Sala de proyección obtenida con éxito.",
            description="Se obtuvo correctamente la sala de proyección solicitada.",
            data=theater
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


@router.post("/", response_model=TheaterResponse)
def create_theater(theater: TheaterRequest):
    """
    Crea una nueva sala de proyección en la base de datos.

    Parámetros:
        - theater (TheaterRequest): Objeto con los datos de la sala de proyección a crear.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos de la sala de proyección creada.
    """
    try:
        created_theater = create_theater_service(theater)
        return TheaterResponse(
            code=200,
            message="La sala de proyección ha sido creada exitosamente.",
            description="La sala de proyección ha sido añadida correctamente a la base de datos.",
            data=created_theater
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{theater_id}", response_model=TheaterResponse)
def update_theater(theater_id: str, theater: TheaterRequest):
    """
    Actualiza una sala de proyección existente en la base de datos.

    Parámetros:
        - theater_id (str): ID de la sala de proyección a actualizar.
        - theater (TheaterRequest): Objeto con los datos actualizados de la sala de proyección.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos de la sala de proyección actualizada.
    """
    try:
        validate_object_id(theater_id)
        updated_theater = update_theater_service(theater_id, theater)
        return TheaterResponse(
            code=200,
            message="La sala de proyección ha sido actualizada exitosamente.",
            description="Los datos de la sala de proyección se han modificado correctamente.",
            data=updated_theater
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


@router.delete("/{theater_id}", response_model=TheaterResponse)
def delete_theater(theater_id: str):
    """
    Elimina una sala de proyección de la base de datos por su ID.

    Parámetros:
        - theater_id (str): ID de la sala de proyección a eliminar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Ninguno.
    """
    try:
        validate_object_id(theater_id)
        delete_theater_service(theater_id)
        return TheaterResponse(
            code=200,
            message="La sala de proyección ha sido eliminada exitosamente.",
            description="Se eliminó correctamente la sala de proyección de la base de datos.",
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
