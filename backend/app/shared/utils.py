from fastapi import HTTPException
from datetime import datetime, date, time

from jose import jwt
from app.database.connection import db
from bson import ObjectId
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Dict


reservations_collection=db["reservations"]
movies_collection=db["movies"]
users_collection = db["users"]


SECRET_KEY = "super53Cr37Pa$$w0rd"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def encode_token(payload: dict) -> str:
    """
    Genera un token JWT basado en el payload proporcionado.

    :param payload: Información a incluir en el token.
    :return: Token JWT codificado como string.
    """
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token:Annotated[str, Depends(oauth2_scheme)]) -> str:
    """
    Decodifica un token JWT para obtener el payload.

    :param token: Token JWT proporcionado.
    :return: Información decodificada del token.
    """
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = users_collection.find_one({"username": data["username"]})
    # user=users.get(data["username"])
    return user


def validate_object_id(id: str) -> ObjectId:
    """
    Valida y convierte un string a un ObjectId de MongoDB.
    Lanza una excepción si el ID no es válido.
    """
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=400,  # Código HTTP para "Bad Request"
            detail={
                "message": "El objeto no fue encontrado o no existe en la base de datos.",
                "description": f"ObjectId inválido: {id}"
            }
        )
    
def validate_reservation_time(start_time: datetime, end_time: datetime):
    """
    Valida que los tiempos de inicio y fin estén dentro del horario permitido (09:00 - 22:00).
    
    Args:
        start_time (datetime): Tiempo de inicio de la reservación.
        end_time (datetime): Tiempo de fin de la reservación.
    
    Raises:
        ValueError: Si el tiempo está fuera del rango permitido.
    """
    # Usar una fecha ficticia para los límites de horario
    open_time = datetime.combine(start_time.date(), time(9, 0))   # 09:00 AM
    close_time = datetime.combine(start_time.date(), time(22, 0)) # 10:00 PM
    
    # Comparar directamente como datetime
    if start_time < open_time or end_time > close_time or end_time < start_time:
        raise ValueError({
            "message": "Horario no permitido",
            "description": "La reservación debe estar entre las 09:00 y las 22:00.",
            "data": None
        })


def validate_theater_availability(theater_id: str, reservation_date: datetime, start_time: datetime, end_time: datetime):
    """
    Verifica si hay conflictos de horarios en un teatro específico y calcula los horarios disponibles del día.

    Args:
        theater_id (str): ID del teatro.
        reservation_date (datetime): Fecha de la reservación.
        start_time (datetime): Hora de inicio de la reservación.
        end_time (datetime): Hora de fin de la reservación.

    Returns:
        list[dict]: Lista de horarios disponibles en formato {"start_time": ..., "end_time": ...}.

    Raises:
        ValueError: Si hay conflictos de horarios en el teatro.
    """
    # Buscar todas las reservaciones que coincidan con el teatro y la fecha
    existing_reservations = list(reservations_collection.find({
        "theater_id": ObjectId(theater_id),
        "reservation_date": reservation_date
    }))

    # Ordenar reservaciones existentes por horario de inicio
    existing_reservations.sort(key=lambda x: x["start_time"])

    # Calcular espacios disponibles
    open_time = datetime.combine(reservation_date.date(), time(9, 0))
    close_time = datetime.combine(reservation_date.date(), time(22, 0))
    end_time = datetime.combine(reservation_date.date(), end_time.time())
    start_time = datetime.combine(reservation_date.date(), start_time.time())
    current_start = open_time
    available_times = []

    for reservation in existing_reservations:
        reservation_start = reservation["start_time"]
        reservation_end = reservation["end_time"]

        # Si hay un espacio disponible antes de la siguiente reservación
        if current_start < reservation_start:
            available_times.append({
                "start_time": current_start.strftime("%H:%M"),
                "end_time": reservation_start.strftime("%H:%M")
            })
        # Mover el inicio actual al final de la reservación actual
        current_start = max(current_start, reservation_end)

    # Verificar si hay espacio después de la última reservación
    if current_start < close_time:
        available_times.append({
            "start_time": current_start.strftime("%H:%M"),
            "end_time": close_time.strftime("%H:%M")
        })

    # Validar conflictos con el horario solicitado
    conflicting_reservations = [
        res for res in existing_reservations
        if res["start_time"] < end_time and res["end_time"] > start_time
    ]

    if conflicting_reservations:
        raise ValueError({
            "message": "No hay disponibilidad en ese horario",
            "description": "La sala de proyección ya tiene reservaciones en este horario, por favor valida los horarios disponibles",
            "data": available_times  # Lista de horarios disponibles acotados
        })


    return

def validate_movie_duration(movie_id: str, start_time: datetime, end_time: datetime):
    """
    Valida si la duración de la película seleccionada permite su reproducción completa en el horario solicitado.

    Args:
        movie_id (str): ID de la película seleccionada.
        start_time (datetime): Hora de inicio de la reservación.
        end_time (datetime): Hora de fin de la reservación.

    Raises:
        ValueError: Si la duración de la película no encaja en el horario seleccionado.
    """
    # Buscar la película en la base de datos
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise ValueError({
            "message": "Película no encontrada",
            "description": f"No se encontró ninguna película con el ID proporcionado: {movie_id}",
            "data": None
        })

    # Obtener la duración de la película en minutos
    movie_duration = movie.get("duration")  # Duración en minutos
    if not movie_duration:
        raise ValueError({
            "message": "Duración no especificada",
            "description": "La película seleccionada no tiene una duración definida.",
            "data": None
        })

    # Calcular la duración del intervalo de tiempo seleccionado
    interval_duration = (end_time - start_time).total_seconds() / 60  # Convertir a minutos

    # Validar si la película cabe en el intervalo
    if movie_duration > interval_duration:
        raise ValueError({
            "message": "Duración insuficiente",
            "description": f"La duración del horario seleccionado ({interval_duration:.0f} minutos) "
                           f"es menor que la duración de la película ({movie_duration} minutos).",
            "data": None
        })
    return 



def convert_time_to_datetime(reservation_date: date, t: time) -> datetime:
    """
    Combina una fecha y una hora en un objeto datetime para MongoDB.
    """
    return datetime.combine(reservation_date, t)

def format_datetime_fields(reservation_data: dict) -> dict:
    """
    Formatea los campos datetime en un diccionario de reservación para 
    devolver tiempos (`start_time`, `end_time`) como `time` 
    y fechas (`reservation_date`) como `date`.

    Args:
        reservation_data (dict): Documento de MongoDB con campos datetime.

    Returns:
        dict: Diccionario con los campos formateados.
    """
    reservation_data["start_time"] = reservation_data["start_time"].time().replace(second=0)  # Hora sin segundos
    reservation_data["end_time"] = reservation_data["end_time"].time().replace(second=0)  
    reservation_data["reservation_date"] = reservation_data["reservation_date"].date()  # Convertir a date
    return reservation_data


def validate_user_unique(username: str, email: str):
    """
    Valida que el nombre de usuario o correo electrónico no existan previamente en la base de datos.

    Descripción:
    Esta función verifica si ya existe un usuario en la base de datos con el mismo nombre de usuario (`username`) 
    o correo electrónico (`email`). Si se detecta un conflicto, se lanza un `ValueError` con un mensaje 
    estructurado que incluye detalles del error.

    Parámetros:
    - username (str): El nombre de usuario proporcionado.
    - email (str): El correo electrónico proporcionado.
    - users_collection (Collection): La colección de MongoDB que contiene los registros de usuarios.

    Respuesta:
    - Si no se detecta un conflicto, no retorna nada.
    - Si el nombre de usuario o correo electrónico ya existen:
        Lanza un ValueError con la siguiente estructura:
        {
            "message": "El usuario ya existe.",
            "description": "El nombre de usuario o correo electrónico ya están registrados en el sistema.",
            "data": {
                "username": <nombre_de_usuario>,
                "email": <correo_electronico>
            }
        }
    """
    existing_user = users_collection.find_one({
        "$or": [
            {"username": username},
            {"email": email}
        ]
    })

    if existing_user:
        raise ValueError({
            "message": "El usuario ya existe.",
            "description": "El nombre de usuario o correo electrónico ya están registrados en el sistema.",
            "data": {
                "username": username,
                "email": email
            }
        })
