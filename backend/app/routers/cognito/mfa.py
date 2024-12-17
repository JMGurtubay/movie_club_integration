from fastapi import APIRouter, HTTPException
from ...schemas.cognito.mfa import VerifyTOTPRequest, VerifyTOTPResponse, VerifyTOTPResponseError
from ...services.cognito.mfa import verify_totp_service
from fastapi import APIRouter, HTTPException
from ...schemas.cognito.mfa import AssociateTOTPRequest, AssociateTOTPResponse, AssociateTOTPResponseError
from ...services.cognito.mfa import associate_totp_service
from fastapi import APIRouter, HTTPException
from ...schemas.cognito.mfa import RespondToChallengeRequest, RespondToChallengeResponse, RespondToChallengeResponseError
from ...services.cognito.mfa import respond_to_auth_challenge_service

router = APIRouter()

@router.post("/verify-totp", response_model=VerifyTOTPResponse, responses={400: {"model": VerifyTOTPResponseError}})
async def verify_totp(request: VerifyTOTPRequest):
    '''
    Descripción:
        API para verificar el código TOTP proporcionado por el usuario. Esta API completa la configuración de TOTP (autenticación multifactor) para el usuario.

    Request:
        - session (str): Sesión actual del usuario iniciada en Cognito.
        - user_code (str): Código TOTP proporcionado por el usuario.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "TOTP configurado".
        - description (str): Descripción del estado de la configuración de TOTP.
    '''
    try:
        return await verify_totp_service(request)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=VerifyTOTPResponseError(
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

@router.post("/associate-totp", response_model=AssociateTOTPResponse, responses={400: {"model": AssociateTOTPResponseError}})
async def associate_totp(request: AssociateTOTPRequest):
    '''
    Descripción:
        API para asociar TOTP al usuario. Genera un código secreto que el usuario puede escanear o introducir en una aplicación de autenticación (como Google Authenticator) para configurar TOTP.

    Request:
        - session (str): Sesión actual del usuario iniciada en Cognito.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Asociación de TOTP exitosa".
        - description (str): Descripción del estado de la asociación de TOTP.
        - secret_code (str): Código secreto para configurar TOTP en una aplicación de autenticación.
        - session (str): Nueva sesión que puede ser utilizada en el flujo de autenticación.
    '''
    try:
        return await associate_totp_service(request)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=AssociateTOTPResponseError(
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
    
@router.post("/respond-to-auth-challenge", response_model=RespondToChallengeResponse, responses={400: {"model": RespondToChallengeResponseError}})
async def respond_to_auth_challenge(request: RespondToChallengeRequest):
    '''
    Descripción:
        API para responder al desafío de autenticación de TOTP. Esta API completa el flujo de autenticación cuando se requiere autenticación multifactor (MFA).

    Request:
        - session (str): Sesión actual del usuario iniciada en Cognito.
        - user_code (str): Código TOTP proporcionado por el usuario.
        - username (str): Nombre de usuario del destinatario.

    Response (caso exitoso):
        - code (int): Código de estado (200).
        - message (str): "Desafío completado con éxito".
        - description (str): Descripción del estado de la autenticación.
        - access_token (str): Token de acceso generado tras la autenticación.
        - id_token (str): ID Token de usuario.
        - refresh_token (str): Token de actualización.
        - token_type (str): Tipo de token (por ejemplo, "Bearer").
    '''
    try:
        return await respond_to_auth_challenge_service(request)
    except ValueError as e:
        error_data = e.args[0]
        raise HTTPException(
            status_code=400,
            detail=RespondToChallengeResponseError(
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