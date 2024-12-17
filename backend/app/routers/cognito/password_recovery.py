from fastapi import APIRouter, HTTPException
from ...schemas.cognito.password_recovery import (
    ForgotPasswordRequest, ConfirmForgotPasswordRequest,
    ForgotPasswordResponse, ForgotPasswordResponseError,
    ConfirmForgotPasswordResponse, ConfirmForgotPasswordResponseError
)
from ...services.cognito.password_recovery import (
    forgot_password_service, confirm_forgot_password_service
)

router = APIRouter()

@router.post("/forgot-password", response_model=ForgotPasswordResponse, responses={404: {"model": ForgotPasswordResponseError}, 400: {"model": ForgotPasswordResponseError}})
async def forgot_password(request: ForgotPasswordRequest):
    '''
    Descripción:
        API para iniciar el proceso de recuperación de contraseña. Envía un código de verificación al correo electrónico o número de teléfono asociado al usuario.

    Request:
        - username (str): Nombre de usuario registrado en el sistema.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Código de verificación enviado".
        - description (str): Explicación de que el código de verificación fue enviado.
    '''
    try:
        return await forgot_password_service(request)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=ForgotPasswordResponseError(
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


@router.post("/confirm-forgot-password", response_model=ConfirmForgotPasswordResponse, responses={400: {"model": ConfirmForgotPasswordResponseError}})
async def confirm_forgot_password(request: ConfirmForgotPasswordRequest):
    '''
    Descripción:
        API para confirmar y completar el proceso de recuperación de contraseña. Verifica el código de recuperación y permite establecer una nueva contraseña.

    Request:
        - username (str): Nombre de usuario registrado.
        - confirmation_code (str): Código de verificación recibido por el usuario.
        - new_password (str): Nueva contraseña que el usuario desea establecer.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Contraseña restablecida".
        - description (str): Indicación de que la contraseña fue restablecida con éxito.
    '''
    try:
        return await confirm_forgot_password_service(request)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=ConfirmForgotPasswordResponseError(
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
