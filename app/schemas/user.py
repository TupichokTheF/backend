from pydantic import BaseModel, Field, field_validator, ConfigDict
from fastapi import Body
from typing import Annotated


class UserBase(BaseModel):
    username: str
    is_seller: bool = False

class UserSignup(UserBase):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: Annotated[str, Field(min_length=6)]

    @field_validator('password')
    @classmethod
    def validate_password(cls, password_: str):
        if password_.upper() == password_:
            raise ValueError('Треубется хотя бы одна буква в нижнем регистре')
        if password_.lower() == password_:
            raise ValueError('Треубется хотя бы одна буква в верхнем регистре')
        if not any(symbol.isdigit() for symbol in password_):
            raise ValueError('Треубется хотя бы одна цифра')
        return password_

class UserAuthentication(UserSignup):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    email: str