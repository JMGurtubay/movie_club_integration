from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.shared.utils.cognito_utils import validate_token_and_get_payload

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware para validar el token de autorización y extraer el usuario autenticado.
    """
    async def dispatch(self, request: Request, call_next):
        authorization: str = request.headers.get("Authorization")
        
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token de autorización no proporcionado")

        token = authorization.split(" ")[1]
        
        try:
            payload = validate_token_and_get_payload(token)
            request.state.user = payload  # Agregamos el usuario al request
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        response = await call_next(request)
        return response
