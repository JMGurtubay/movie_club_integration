from app.shared.utils import generate_secret_hash
from ...schemas.cognito.password_recovery import (
    ForgotPasswordRequest, ConfirmForgotPasswordRequest,
    ForgotPasswordResponse, ConfirmForgotPasswordResponse
)
from botocore.exceptions import ClientError
from app.shared.config import USER_POOL_ID, CLIENT_ID, client, CLIENT_SECRET




async def forgot_password_service(request: ForgotPasswordRequest) -> ForgotPasswordResponse:
    """
    Lógica de negocio para iniciar el proceso de recuperación de contraseña.
    """
    secret_hash = generate_secret_hash(request.username, CLIENT_ID, CLIENT_SECRET)

    try:
        client.forgot_password(
            ClientId=CLIENT_ID,
            Username=request.username,
            SecretHash=secret_hash
        )
        return ForgotPasswordResponse(
            code=200,
            message="Código de verificación enviado",
            description="Código de verificación enviado al correo o número de teléfono asociado."
        )
    except client.exceptions.UserNotFoundException:
        raise ValueError({
            "message": "Usuario no encontrado",
            "description": "No se encontró un usuario con el nombre de usuario proporcionado."
        })
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })


async def confirm_forgot_password_service(request: ConfirmForgotPasswordRequest) -> ConfirmForgotPasswordResponse:
    """
    Lógica de negocio para confirmar y completar el proceso de recuperación de contraseña.
    """
    secret_hash = generate_secret_hash(request.username, CLIENT_ID, CLIENT_SECRET)
    try:
        client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=request.username,
            ConfirmationCode=request.confirmation_code,
            Password=request.new_password,
            SecretHash=secret_hash

        )
        return ConfirmForgotPasswordResponse(
            code=200,
            message="Contraseña restablecida",
            description="Contraseña restablecida con éxito."
        )
    except client.exceptions.CodeMismatchException:
        raise ValueError({
            "message": "Código incorrecto",
            "description": "El código de verificación es incorrecto."
        })
    except client.exceptions.ExpiredCodeException:
        raise ValueError({
            "message": "Código expirado",
            "description": "El código de verificación ha expirado."
        })
    except client.exceptions.InvalidPasswordException:
        raise ValueError({
            "message": "Contraseña no válida",
            "description": "La nueva contraseña no cumple con los requisitos de seguridad."
        })
    except client.exceptions.UserNotFoundException:
        raise ValueError({
            "message": "Usuario no encontrado",
            "description": "No se encontró un usuario con el nombre de usuario proporcionado."
        })
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })
