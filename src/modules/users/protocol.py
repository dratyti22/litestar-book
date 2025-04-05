from abc import abstractmethod
from typing import Protocol

from src.modules.users.model import UserDb
from src.modules.users.schema import RegisterUserDTO, LoginUserDTO


class UserProtocol(Protocol):
    @abstractmethod
    async def register(self, data: RegisterUserDTO) -> UserDb: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserDb: ...

    @abstractmethod
    async def login_user(self, data: LoginUserDTO) -> UserDb: ...
