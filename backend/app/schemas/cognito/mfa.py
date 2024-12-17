from pydantic import BaseModel

# Modelo para la solicitud de verificación de TOTP
class VerifyTOTPRequest(BaseModel):
    session: str
    user_code: str

# Modelo para la respuesta exitosa
class VerifyTOTPResponse(BaseModel):
    code: int
    message: str
    description: str

# Modelo para la respuesta de error
class VerifyTOTPResponseError(BaseModel):
    code: int
    message: str
    description: str


from pydantic import BaseModel

# Modelo para la solicitud de asociación de TOTP
class AssociateTOTPRequest(BaseModel):
    session: str

# Modelo para la respuesta exitosa
class AssociateTOTPResponse(BaseModel):
    code: int
    message: str
    description: str
    secret_code: str
    session: str

# Modelo para la respuesta de error
class AssociateTOTPResponseError(BaseModel):
    code: int
    message: str
    description: str


from pydantic import BaseModel

# Modelo para la solicitud de respuesta al desafío
class RespondToChallengeRequest(BaseModel):
    session: str
    user_code: str
    username: str

# Modelo para la respuesta exitosa
class RespondToChallengeResponse(BaseModel):
    code: int
    message: str
    description: str
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str

# Modelo para la respuesta de error
class RespondToChallengeResponseError(BaseModel):
    code: int
    message: str
    description: str
