from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import post, Response
from litestar.controller import Controller
from litestar.exceptions import HTTPException
from litestar.security.jwt import Token

from src.modules.users.auth import oauth2
from src.modules.users.protocol import UserProtocol
from src.modules.users.schema import RegisterUserDTO, LoginUserDTO, UserResponseDTO


class UserController(Controller):
    path = '/user'
    tags = ["User"]

    @post("/register", tags="User")
    @inject
    async def register(self, data: RegisterUserDTO, service: FromDishka[UserProtocol]) -> UserResponseDTO:
        user_db = await service.register(data)
        return UserResponseDTO.model_validate(user_db)

    @post("/login", tags="User", status_code=200, exclude_from_auth=True)
    @inject
    async def login_user(self, data: LoginUserDTO, service: FromDishka[UserProtocol]) -> Response[Token]:
        try:
            user = await service.login_user(data)
            print(user.id)
            return oauth2.login(identifier=str(user.id))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                detail="Login failed",
                status_code=500
            ) from e
