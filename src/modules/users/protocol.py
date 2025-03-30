from abc import abstractmethod
from typing import Protocol

from src.modules.users.model import UserDb
from src.modules.users.schema import RegisterUserDTO, UserResponseDTO, LoginUserDTO


class UserProtocol(Protocol):
    @abstractmethod
    async def register(self, data: RegisterUserDTO) -> UserResponseDTO: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserResponseDTO: ...

    @abstractmethod
    async def login(self, data: LoginUserDTO) -> int: ...
