from pydantic import BaseModel, Field, field_validator
from typing import Annotated


class UserBase(BaseModel):
    username: str
    is_seller: bool

class UserAuthentication(UserBase):
    email: str
    password: Annotated[str, Field(min_length=6, max_length=30)]

    @field_validator('password')
    @classmethod
    def validate_password(cls, password_: str):
        if password_.upper() == password_:
            raise ValueError('Треубется хотя бы одна буква в верхнем регистре')
        if password_.lower() == password_:
            raise ValueError('Треубется хотя бы одна буква в нижнем регистре')
        if not any(symbol.isdigit() for symbol in password_):
            raise ValueError('Треубется хотя бы одна цифра')