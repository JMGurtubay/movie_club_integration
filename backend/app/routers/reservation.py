from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.reservation import ReservationRequest, ReservationResponse
from app.services.reservation import create_reservation_service,get_all_reservations_service,get_reservation_by_id_service,delete_reservation_service,update_reservation_service
from app.shared.utils import decode_token, validate_object_id, validate_reservation_time, validate_theater_availability,validate_movie_duration
from app.shared.exceptions import BusinessLogicError

router = APIRouter()

@router.get("/", response_model=ReservationResponse)
def get_reservations():
    """
    Obtiene la lista de todas las reservaciones.

    Parámetros:
        - Ninguno.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Lista de reservaciones obtenidas.
    """
    try:
        reservations = get_all_reservations_service()
        return ReservationResponse(
            code=200,
            message="Reservaciones obtenidas con éxito.",
            description="Se obtuvo correctamente la lista de reservaciones.",
            data=reservations
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: str):
    """
    Obtiene una reservación específica por su ID.

    Parámetros:
        - reservation_id (str): ID de la reservación a buscar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Datos de la reservación encontrada.
    """
    try:
        validate_object_id(reservation_id)
        reservation = get_reservation_by_id_service(reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Reservación no encontrada.",
                    "description": "No se encontró una reservación con el ID proporcionado."
                }
            )
        return ReservationResponse(
            code=200,
            message="Reservación obtenida con éxito.",
            description="Se obtuvo correctamente la reservación solicitada.",
            data=reservation
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


@router.post("/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationRequest):
    """
    Crea una nueva reservación en la base de datos.

    Parámetros:
        - reservation (ReservationRequest): Objeto con los datos de la reservación a crear.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos de la reservación creada.
    """
    try:
        validate_reservation_time(reservation.start_time, reservation.end_time)
        validate_theater_availability(
            reservation.theater_id,
            reservation.reservation_date,
            reservation.start_time,
            reservation.end_time
        )
        validate_movie_duration(
            reservation.movie_id,
            reservation.start_time,
            reservation.end_time
        )
        created_reservation = create_reservation_service(reservation, str(user["_id"]))

        return ReservationResponse(
            code=200,
            message="La reservación ha sido creada exitosamente.",
            description="La reservación se añadió correctamente a la base de datos.",
            data=created_reservation,
        )
    except ValueError as e:
        error_data = e.args[0]
        raise BusinessLogicError(
            message=error_data["message"],
            description=error_data["description"],
            data=error_data["data"]
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(reservation_id: str, reservation: ReservationRequest):
    """
    Actualiza una reservación existente en la base de datos.

    Parámetros:
        - reservation_id (str): ID de la reservación a actualizar.
        - reservation (ReservationRequest): Objeto con los datos actualizados de la reservación.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Objeto con los datos de la reservación actualizada.
    """
    try:
        validate_object_id(reservation_id)
        updated_reservation = update_reservation_service(reservation_id, reservation)
        return ReservationResponse(
            code=200,
            message="La reservación ha sido actualizada exitosamente.",
            description="Los datos de la reservación se han modificado correctamente.",
            data=updated_reservation
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


@router.delete("/{reservation_id}", response_model=ReservationResponse)
def delete_reservation(reservation_id: str):
    """
    Elimina una reservación de la base de datos por su ID.

    Parámetros:
        - reservation_id (str): ID de la reservación a eliminar.

    Respuesta:
        - code: Código de estado de la operación (200 si es exitoso).
        - message: Mensaje indicando el resultado de la operación.
        - description: Descripción detallada del resultado.
        - data: Ninguno.
    """
    try:
        validate_object_id(reservation_id)
        delete_reservation_service(reservation_id)
        return ReservationResponse(
            code=200,
            message="La reservación ha sido eliminada exitosamente.",
            description="Se eliminó correctamente la reservación de la base de datos.",
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
