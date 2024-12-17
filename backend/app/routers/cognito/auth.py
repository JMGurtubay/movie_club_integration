from ...schemas.cognito.auth import RegisterResponse, RegisterResponseError, User
from ...services.cognito.auth import register_user_service
from ...schemas.cognito.auth import LoginRequest, LoginResponse, LoginResponseError
from ...services.cognito.auth import login_user_service
from ...schemas.cognito.auth import ConfirmEmail, ConfirmEmailResponse, ConfirmEmailResponseError
from ...services.cognito.auth import confirm_email_service
from fastapi import APIRouter, HTTPException, Request
from ...schemas.cognito.auth import LogoutResponse, LogoutResponseError
from ...services.cognito.auth import logout_user_service



router = APIRouter()

@router.post("/register", response_model=RegisterResponse, responses={400: {"model": RegisterResponseError}})
async def register_user(user: User):
    """
    Descripción:
        API para registrar un nuevo usuario en el sistema mediante AWS Cognito.
    """
    try:
        return await register_user_service(user)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=RegisterResponseError(
                code=400,
                message=error_data["message"],
                description=error_data["description"]
            ).dict()
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/login", response_model=LoginResponse, responses={401: {"model": LoginResponseError}, 400: {"model": LoginResponseError}})
async def login(user: LoginRequest):
    '''
    Descripción:
        API para autenticar a un usuario. Esta API inicia el flujo de autenticación en AWS Cognito y puede requerir MFA (autenticación multifactor).

    Request:
        - username (str): Nombre de usuario.
        - password (str): Contraseña del usuario.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Inicio de sesión exitoso" o mensajes relacionados con la configuración de MFA.
        - description (str): Descripción del estado de autenticación.
        - data (dict): Información adicional, incluyendo un token de acceso o la sesión MFA requerida.
    '''
    try:
        return await login_user_service(user)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=LoginResponseError(
                code=400,
                message=error_data["message"],
                description=error_data["description"]
            ).dict()
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post("/confirm-email", response_model=ConfirmEmailResponse, responses={400: {"model": ConfirmEmailResponseError}})
async def confirm_email(data: ConfirmEmail):
    '''
    Descripción:
        API para confirmar el correo electrónico de un usuario mediante un código de verificación enviado por correo electrónico.

    Request:
        - username (str): Nombre de usuario del destinatario.
        - confirmation_code (str): Código de verificación recibido en el correo electrónico.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Email confirmado".
        - description (str): Descripción del estado de la confirmación.
    '''
    try:
        return await confirm_email_service(data)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=ConfirmEmailResponseError(
                code=400,
                message=error_data["message"],
                description=error_data["description"]
            ).dict()
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post("/logout", response_model=LogoutResponse, responses={401: {"model": LogoutResponseError}, 400: {"model": LogoutResponseError}})
async def logout(request: Request):
    '''
    Descripción:
        API para cerrar la sesión del usuario. Invalida el token de acceso del usuario en AWS Cognito.

    Request:
        - Authorization (str): Token de acceso del usuario en el encabezado de la solicitud, en formato "Bearer {access_token}".

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Sesión cerrada".
        - description (str): Descripción del estado del cierre de sesión.
    '''
    access_token = request.headers.get("Authorization")
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail=LogoutResponseError(
                code=401,
                message="Token no proporcionado",
                description="El token de acceso no fue proporcionado o es inválido."
            ).dict()
        )

    access_token = access_token.split(" ")[1]

    try:
        return await logout_user_service(access_token)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=LogoutResponseError(
                code=400,
                message=error_data["message"],
                description=error_data["description"]
            ).dict()
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )