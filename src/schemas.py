from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequest(BaseModel):
    username: str
    password: str
    name: str
    email: EmailStr
    phone: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    phone: str
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
