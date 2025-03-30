from src.modules.users.model import UserDb
from src.modules.users.protocol import UserProtocol
from src.modules.users.repository import UserRepository
from src.modules.users.schema import RegisterUserDTO, UserResponseDTO, LoginUserDTO


class UserService(UserProtocol):
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register(self, data: RegisterUserDTO) -> UserResponseDTO:
        return await self.repository.register(data)

    async def get_user_by_id(self, user_id: int) -> UserResponseDTO:
        return await self.repository.get_user_by_id(user_id)

    async def login(self, data: LoginUserDTO) -> int:
        return await self.repository.login(data)
