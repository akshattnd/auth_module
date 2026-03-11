from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict
)

class LoginRequest(BaseModel):
    email:EmailStr
    password:str
    model_config = ConfigDict(str_strip_whitespace=True)

class TokenResponse(BaseModel):
    access_token:str
    token_type:str = 'Bearer'