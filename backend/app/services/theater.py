from typing import List
from app.database.connection import db
from app.models.theater import TheaterDB
from app.schemas.theater import TheaterRequest
from pymongo.errors import PyMongoError
from bson import ObjectId

theaters_collection = db["theaters"]

def get_all_theaters_service() -> List[TheaterDB]:
    try:
        theaters_cursor = theaters_collection.find({})
        theaters = [
            TheaterDB(
                id=str(theater["_id"]),
                name=theater["name"],
                max_capacity=theater["max_capacity"],
                projection=theater["projection"],
                screen_size=theater["screen_size"],
                description=theater["description"],
            )
            for theater in theaters_cursor
        ]
        return theaters
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_theater_by_id_service(theater_id: str) -> TheaterDB:
    try:
        theater = theaters_collection.find_one({"_id": ObjectId(theater_id)})
        if not theater:
            return None
        return TheaterDB(
            id=str(theater["_id"]),
            name=theater["name"],
            max_capacity=theater["max_capacity"],
            projection=theater["projection"],
            screen_size=theater["screen_size"],
            description=theater["description"],
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_theater_service(theater_data: TheaterRequest)-> TheaterDB:
    try:
        result = theaters_collection.insert_one(theater_data.model_dump(exclude={"id"}))

        created_theater = theaters_collection.find_one({"_id": result.inserted_id})

        return TheaterDB(
            id=str(created_theater["_id"]),
            name=created_theater["name"],
            max_capacity=created_theater["max_capacity"],
            projection=created_theater["projection"],
            screen_size=created_theater["screen_size"],
            description=created_theater["description"],
        )

    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def update_theater_service(theater_id: str, theater_data: TheaterRequest) -> TheaterDB:
    try:
        result = theaters_collection.update_one(
            {"_id": ObjectId(theater_id)},
            {"$set": theater_data.model_dump(exclude={"id"})}
        )

        if result.matched_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {theater_id}")

        updated_theater = theaters_collection.find_one({"_id": ObjectId(theater_id)})

        return TheaterDB(**updated_theater)
        
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def delete_theater_service(theater_id: str) -> bool:
    try:

 
        result = theaters_collection.delete_one({"_id": ObjectId(theater_id)})

  
        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ninguna película con el ID proporcionado: {theater_id}")

        return True 

    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

