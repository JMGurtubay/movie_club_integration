from pydantic import BaseModel, EmailStr

# Modelo para la solicitud de registro
class User(BaseModel):
    username: str
    email: EmailStr
    password: str

# Modelo para la respuesta exitosa
class RegisterResponse(BaseModel):
    code: int
    message: str
    description: str

# Modelo para la respuesta de error
class RegisterResponseError(BaseModel):
    code: int
    message: str
    description: str


from pydantic import BaseModel

# Modelo para la solicitud de login
class LoginRequest(BaseModel):
    username: str
    password: str

# Modelo para la respuesta exitosa
class LoginResponse(BaseModel):
    code: int
    message: str
    description: str
    data: dict

# Modelo para la respuesta de error
class LoginResponseError(BaseModel):
    code: int
    message: str
    description: str


from pydantic import BaseModel

# Modelo para la solicitud de confirmación de email
class ConfirmEmail(BaseModel):
    username: str
    confirmation_code: str

# Modelo para la respuesta exitosa
class ConfirmEmailResponse(BaseModel):
    code: int
    message: str
    description: str

# Modelo para la respuesta de error
class ConfirmEmailResponseError(BaseModel):
    code: int
    message: str
    description: str

from pydantic import BaseModel

# Modelo para la respuesta exitosa
class LogoutResponse(BaseModel):
    code: int
    message: str
    description: str

# Modelo para la respuesta de error
class LogoutResponseError(BaseModel):
    code: int
    message: str
    description: str
