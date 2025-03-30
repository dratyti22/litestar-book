from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import post, Response, Request
from litestar.controller import Controller
from litestar.security.jwt import Token

from src.modules.users.auth import o2auth
from src.modules.users.protocol import UserProtocol
from src.modules.users.schema import RegisterUserDTO, LoginUserDTO, UserResponseDTO


class UserController(Controller):
    path = '/user'
    tags = ["User"]

    @post("/register", tags="User")
    @inject
    async def register(self, data: RegisterUserDTO, service: FromDishka[UserProtocol]) -> UserResponseDTO:
        return await service.register(data)

    @post("/login", tags="User", status_code=200)
    @inject
    async def login(self, data: LoginUserDTO, service: FromDishka[UserProtocol]) -> Response[Token]:
        user_id = await service.login(data)
        return o2auth.login(identifier=str(user_id))
