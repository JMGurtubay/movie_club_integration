from ...schemas.cognito.auth import RegisterResponse, User
from botocore.exceptions import ClientError
from app.shared.utils import generate_secret_hash
from app.shared.config import USER_POOL_ID, CLIENT_ID, client, CLIENT_SECRET
from ...schemas.cognito.auth import LoginRequest, LoginResponse
from ...schemas.cognito.auth import ConfirmEmail, ConfirmEmailResponse
from ...schemas.cognito.auth import LogoutResponse


async def register_user_service(user: User) -> RegisterResponse:
    """
    Lógica de negocio para registrar un usuario en AWS Cognito.
    """
    secret_hash = generate_secret_hash(user.username, CLIENT_ID, CLIENT_SECRET)
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=secret_hash,
            Username=user.username,
            Password=user.password,
            UserAttributes=[
                {
                    "Name": "email",
                    "Value": user.email
                }
            ]
        )
        return RegisterResponse(
            code=200,
            message="Registro exitoso",
            description="Usuario registrado. Se ha enviado un correo de verificación al email proporcionado."
        )
    except client.exceptions.UsernameExistsException:
        raise ValueError({
            "message": "Nombre de usuario ya existente",
            "description": "El nombre de usuario ya existe."
        })
    except ClientError as e:
        raise RuntimeError(f"Error en AWS Cognito: {str(e)}")




async def login_user_service(user: LoginRequest) -> LoginResponse:
    """
    Lógica de negocio para autenticar a un usuario en AWS Cognito.
    """
    secret_hash = generate_secret_hash(user.username, CLIENT_ID, CLIENT_SECRET)
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": user.username,
                "PASSWORD": user.password,
                "SECRET_HASH": secret_hash
            }
        )
        if 'ChallengeName' in response and response['ChallengeName'] == 'MFA_SETUP':
            print(response)
            return LoginResponse(
                code=200,
                message="Configuración de MFA requerida",
                description="El usuario necesita configurar MFA.",
                data={"session": response['Session']}
            )

        if 'ChallengeName' in response and response['ChallengeName'] == 'SOFTWARE_TOKEN_MFA':
            return LoginResponse(
                code=200,
                message="Se requiere TOTP",
                description="Se requiere un código TOTP para completar el inicio de sesión.",
                data={"session": response['Session']}
            )

        return LoginResponse(
            code=200,
            message="Inicio de sesión exitoso",
            description="El usuario ha iniciado sesión correctamente.",
            data=response.get('AuthenticationResult', {})
        )

    except client.exceptions.NotAuthorizedException:
        raise ValueError({
            "message": "Credenciales incorrectas",
            "description": "El nombre de usuario o la contraseña son incorrectos."
        })
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })





async def confirm_email_service(data: ConfirmEmail) -> ConfirmEmailResponse:
    """
    Lógica de negocio para confirmar el email de un usuario en AWS Cognito.
    """
    secret_hash = generate_secret_hash(data.username, CLIENT_ID, CLIENT_SECRET)
    try:
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=secret_hash,
            Username=data.username,
            ConfirmationCode=data.confirmation_code
        )
        return ConfirmEmailResponse(
            code=200,
            message="Email confirmado",
            description="Email confirmado exitosamente. La cuenta está ahora activa."
        )
    except client.exceptions.CodeMismatchException:
        raise ValueError({
            "message": "Código incorrecto",
            "description": "El código de verificación es incorrecto."
        })
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })




async def logout_user_service(access_token: str) -> LogoutResponse:
    """
    Lógica de negocio para cerrar la sesión de un usuario en AWS Cognito.
    """
    try:
        client.global_sign_out(AccessToken=access_token)
        return LogoutResponse(
            code=200,
            message="Sesión cerrada",
            description="Sesión cerrada con éxito."
        )
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })
