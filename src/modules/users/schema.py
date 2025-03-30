from decimal import Decimal

from litestar.dto import DTOConfig
from pydantic import BaseModel, SecretStr, EmailStr

from src.modules.books.schema import BookDTO


class UserResponseDTO(BaseModel):
    id: int
    email: str
    deposit: Decimal
    books: list[BookDTO] = None

    class Config:
        dto_config = DTOConfig(
            exclude={"password"},
        )
        from_attributes = True


class RegisterUserDTO(BaseModel):
    email: EmailStr
    password: SecretStr

class LoginUserDTO(BaseModel):
    email: EmailStr
    password: SecretStr
