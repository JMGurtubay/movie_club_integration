from datetime import datetime
from typing import List
from pymongo.errors import PyMongoError
from bson import ObjectId
from app.models.reservation import ReservationDB
from app.schemas.reservation import ReservationRequest
from app.database.connection import db

reservations_collection = db["reservations"]

def get_all_reservations_service() -> List[ReservationDB]:
    try:
        reservations_cursor = reservations_collection.find({})
        reservations = [
            ReservationDB(
                id=str(reservation["_id"]),
                user_id=str(reservation["user_id"]),
                theater_id=str(reservation["theater_id"]),
                movie_id=str(reservation["movie_id"]),
                is_private=reservation["is_private"],
                start_time=reservation["start_time"],
                end_time=reservation["end_time"],
                reservation_date=reservation["reservation_date"],
                status=reservation["status"],
            )
            for reservation in reservations_cursor
        ]
        return reservations
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_reservation_by_id_service(reservation_id: str) -> ReservationDB:
    try:
        reservation = reservations_collection.find_one({"_id": ObjectId(reservation_id)})
        if not reservation:
            return None
        return ReservationDB(
            id=str(reservation["_id"]),
            user_id=str(reservation["user_id"]),
            theater_id=str(reservation["theater_id"]),
            movie_id=str(reservation["movie_id"]),
            is_private=reservation["is_private"],
            start_time=reservation["start_time"],
            end_time=reservation["end_time"],
            reservation_date=reservation["reservation_date"],
            status=reservation["status"],
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_reservation_service(reservation_data: ReservationRequest, user_id:StopAsyncIteration) -> ReservationDB:
    try:
        
        reservation_data.validate_fields()
        reservation_dict = reservation_data.model_dump(exclude={"id"})
        reservation_dict["user_id"] = ObjectId(user_id)
        reservation_dict["theater_id"] = ObjectId(reservation_dict["theater_id"])
        reservation_dict["movie_id"] = ObjectId(reservation_dict["movie_id"])
        reservation_dict["start_time"]= datetime.combine(reservation_dict["reservation_date"].date(), reservation_dict["start_time"].time())
        reservation_dict["end_time"]= datetime.combine(reservation_dict["reservation_date"].date(), reservation_dict["end_time"].time())

        result = reservations_collection.insert_one(reservation_dict)

        
        created_reservation = reservations_collection.find_one({"_id": result.inserted_id})

        return ReservationDB(
            id=str(created_reservation["_id"]),
            user_id=str(created_reservation["user_id"]),
            theater_id=str(created_reservation["theater_id"]),
            movie_id=str(created_reservation["movie_id"]),
            is_private=created_reservation["is_private"],
            start_time=created_reservation["start_time"],
            end_time=created_reservation["end_time"],
            reservation_date=created_reservation["reservation_date"].strftime("%Y-%m-%d"),
            status=created_reservation["status"],
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def update_reservation_service(reservation_id: str, reservation_data: ReservationRequest) -> ReservationDB:
    try:
        reservation_data.validate_fields()
        reservation_dict = reservation_data.model_dump()
        reservation_dict["user_id"] = ObjectId(reservation_dict["user_id"])
        reservation_dict["theater_id"] = ObjectId(reservation_dict["theater_id"])
        reservation_dict["movie_id"] = ObjectId(reservation_dict["movie_id"])
        

        result = reservations_collection.update_one(
            {"_id": ObjectId(reservation_id)},
            {"$set": reservation_data.model_dump()}
        )

        
        if result.matched_count == 0:
            raise ValueError(f"No se encontró ninguna reservación con el ID proporcionado: {reservation_id}")

        
        updated_reservation = reservations_collection.find_one({"_id": ObjectId(reservation_id)})

        formatted_reservation = {
            "user_id": str(updated_reservation["user_id"]),
            "theater_id": str(updated_reservation["theater_id"]), 
            "movie_id": str(updated_reservation["movie_id"]), 
            "is_private": updated_reservation["is_private"],
            "start_time": updated_reservation["start_time"],
            "end_time": updated_reservation["end_time"],
            "reservation_date": updated_reservation["reservation_date"],
            "status": updated_reservation["status"],
        }
        
        return ReservationDB(**formatted_reservation)

        
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def delete_reservation_service(reservation_id: str) -> bool:
    try:

        
        result = reservations_collection.delete_one({"_id": ObjectId(reservation_id)})

        
        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {reservation_id}")

        return True 

    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")
