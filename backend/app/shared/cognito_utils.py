import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.shared.config import REGION_NAME, client

# Cliente de Cognito

def get_user_from_token(access_token: str):
    """
    Valida el access_token con Cognito y obtiene la información del usuario (username).
    """
    try:
        response = client.get_user(AccessToken=access_token)
        username = response.get("Username")
        loquesea=response.get("UserAttributes")
        print(loquesea)
        return username
    except ClientError as e:
        error_message = e.response['Error']['Message']
        raise HTTPException(status_code=401, detail=f"Token inválido o expirado: {error_message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
