from decimal import Decimal

from litestar.dto import DTOConfig
from pydantic import BaseModel, SecretStr, EmailStr

from src.modules.books.schema import BookDTO
from src.modules.users.role import UserRole


class UserResponseDTO(BaseModel):
    id: int
    email: str
    deposit: Decimal
    books: list[BookDTO] = None
    is_activate: bool
    role: UserRole

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
