from app.shared.utils import generate_secret_hash
from ...schemas.cognito.mfa import VerifyTOTPRequest, VerifyTOTPResponse
from botocore.exceptions import ClientError
from ...schemas.cognito.mfa import RespondToChallengeRequest, RespondToChallengeResponse
from ...schemas.cognito.mfa import AssociateTOTPRequest, AssociateTOTPResponse
from app.shared.config import USER_POOL_ID, CLIENT_ID, client, CLIENT_SECRET

# Configuración del cliente de Cognito

async def verify_totp_service(request: VerifyTOTPRequest) -> VerifyTOTPResponse:
    """
    Lógica de negocio para verificar el código TOTP en AWS Cognito.
    """
    try:
        response = client.verify_software_token(
            Session=request.session,
            UserCode=request.user_code
        )
        if response['Status'] == 'SUCCESS':
            return VerifyTOTPResponse(
                code=200,
                message="TOTP configurado",
                description="TOTP configurado correctamente."
            )
        else:
            raise ValueError({
                "message": "Verificación fallida",
                "description": "Verificación de TOTP fallida."
            })
    except client.exceptions.InvalidParameterException:
        raise ValueError({
            "message": "Parámetros inválidos",
            "description": "Código TOTP o sesión inválidos."
        })
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })
    


# Configuración del cliente de Cognito

async def associate_totp_service(request: AssociateTOTPRequest) -> AssociateTOTPResponse:
    """
    Lógica de negocio para asociar TOTP al usuario en AWS Cognito.
    """
    try:
        response = client.associate_software_token(
            Session=request.session
        )
        return AssociateTOTPResponse(
            code=200,
            message="Asociación de TOTP exitosa",
            description="Se ha generado un código secreto para configurar TOTP.",
            secret_code=response['SecretCode'],
            session=response['Session']
        )
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })




async def respond_to_auth_challenge_service(request: RespondToChallengeRequest) -> RespondToChallengeResponse:
    """
    Lógica de negocio para responder al desafío de autenticación de TOTP en AWS Cognito.
    """
    secret_hash = generate_secret_hash(request.username, CLIENT_ID, CLIENT_SECRET)
    try:
        response = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName='SOFTWARE_TOKEN_MFA',
            Session=request.session,
            ChallengeResponses={
                'USERNAME': request.username,
                'SOFTWARE_TOKEN_MFA_CODE': request.user_code,
                'SECRET_HASH':secret_hash
            }
        )
        if 'AuthenticationResult' in response:
            return RespondToChallengeResponse(
                code=200,
                message="Desafío completado con éxito",
                description="El usuario ha completado el desafío TOTP correctamente.",
                access_token=response['AuthenticationResult']['AccessToken'],
                id_token=response['AuthenticationResult']['IdToken'],
                refresh_token=response['AuthenticationResult']['RefreshToken'],
                token_type=response['AuthenticationResult']['TokenType']
            )
        else:
            raise ValueError({
                "message": "Desafío no completado",
                "description": "El desafío no fue completado correctamente."
            })
    except client.exceptions.NotAuthorizedException:
        raise ValueError({
            "message": "Código TOTP incorrecto",
            "description": "El código TOTP proporcionado es incorrecto."
        })
    except ClientError as e:
        raise RuntimeError({
            "message": "Error de Cognito",
            "description": e.response['Error']['Message']
        })
