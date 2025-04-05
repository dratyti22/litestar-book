from decimal import Decimal
from argon2 import PasswordHasher
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_401_UNAUTHORIZED

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.model import UserDb
from src.modules.users.protocol import UserProtocol
from src.modules.users.schema import RegisterUserDTO, LoginUserDTO


class UserRepository(UserProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, data: RegisterUserDTO) -> UserDb:
        hasher = PasswordHasher()
        user = UserDb(
            email=str(data.email),
            password=hasher.hash(data.password.get_secret_value()),
            deposit=Decimal(0.00)
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user, ["books"])
        return user

    async def get_user_by_id(self, user_id: int) -> UserDb:
        user = await self.session.get(UserDb, user_id)
        return user

    async def login_user(self, data: LoginUserDTO) -> UserDb:
        hasher = PasswordHasher()
        print(1)
        result = await self.session.execute(
            select(UserDb).where(UserDb.email == str(data.email)))
        print(3)
        user = result.scalar_one_or_none()
        print(2)
        if not user or not hasher.verify(
            user.password,
            data.password.get_secret_value(),
        ):
            raise HTTPException(
                detail="Invalid credentials",
                status_code=HTTP_401_UNAUTHORIZED
            )
        return user

