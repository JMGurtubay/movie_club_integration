from typing import List
from datetime import datetime
from app.database.connection import db
from app.models.comment import CommentDB
from app.schemas.comment import CommentRequest, CommentUpdateRequest
from pymongo.errors import PyMongoError
from bson import ObjectId

comments_collection = db["comments"]

def get_all_comments_service() -> List[CommentDB]:
    try:
        comments_cursor = comments_collection.find({})
        comments = [
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
        return comments
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def get_comment_by_id_service(comment_id: str) -> CommentDB:
    try:
        comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            return None
        return CommentDB(
            id=str(comment["_id"]),
            user_id=comment["user_id"],
            movie_id=comment["movie_id"],
            parent_comment_id=comment.get("parent_comment_id"),
            comment_content=comment["comment_content"],
            created_at=comment["created_at"],
            updated_at=comment.get("updated_at")
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def create_comment_service(comment_data: CommentRequest) -> CommentDB:
    try:
        comment_dict = comment_data.model_dump()
        comment_dict["created_at"] = datetime.utcnow()
        
        result = comments_collection.insert_one(comment_dict)
        created_comment = comments_collection.find_one({"_id": result.inserted_id})
        
        return CommentDB(
            id=str(created_comment["_id"]),
            user_id=created_comment["user_id"],
            movie_id=created_comment["movie_id"],
            parent_comment_id=created_comment.get("parent_comment_id"),
            comment_content=created_comment["comment_content"],
            created_at=created_comment["created_at"],
            updated_at=created_comment.get("updated_at")
        )
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def update_comment_service(comment_id: str, comment_data: CommentUpdateRequest) -> CommentDB:
    try:
        update_data = comment_data.model_dump()
        update_data["updated_at"] = datetime.utcnow()
        
        result = comments_collection.update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"No se encontró ningún comentario con el ID proporcionado: {comment_id}")
            
        updated_comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
        return CommentDB(**updated_comment)
        
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")

def delete_comment_service(comment_id: str) -> bool:
    try:
        result = comments_collection.delete_one({"_id": ObjectId(comment_id)})
        
        if result.deleted_count == 0:
            raise ValueError(f"No se encontró ningún comentario con el ID proporcionado: {comment_id}")
            
        return True
        
    except PyMongoError as e:
        raise RuntimeError(f"Database error: {str(e)}")