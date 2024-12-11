from fastapi import HTTPException

class BusinessLogicError(HTTPException):
    def __init__(self, message: str, description: str = None, data: dict = None):
        # Construir el detalle del error como un diccionario
        detail = {
            "message": message,
            "description": description,
            "data": data
        }
        super().__init__(status_code=400, detail=detail)
