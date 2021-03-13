from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr


class UserRegisterSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
