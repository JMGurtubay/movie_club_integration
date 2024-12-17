from pydantic import BaseModel

# Modelo para la solicitud de forgot-password
class ForgotPasswordRequest(BaseModel):
    username: str

# Modelo para la respuesta de forgot-password
class ForgotPasswordResponse(BaseModel):
    code: int
    message: str
    description: str

# Modelo para la respuesta de error de forgot-password
class ForgotPasswordResponseError(BaseModel):
    code: int
    message: str
    description: str

# Modelo para la solicitud de confirm-forgot-password
class ConfirmForgotPasswordRequest(BaseModel):
    username: str
    confirmation_code: str
    new_password: str

# Modelo para la respuesta de confirm-forgot-password
class ConfirmForgotPasswordResponse(BaseModel):
    code: int
    message: str
    description: str

# Modelo para la respuesta de error de confirm-forgot-password
class ConfirmForgotPasswordResponseError(BaseModel):
    code: int
    message: str
    description: str
