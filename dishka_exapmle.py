from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from dishka import Provider, provide, Scope, make_container


@dataclass
class Settings:
    url: str


class UserGateway(Protocol):
    @abstractmethod
    def hello_world(self) -> str: ...


class UserGatewayImpl(UserGateway):
    def __init__(self, conn: Settings) -> None:
        self.conn = conn

    def hello_world(self) -> str:
        return f"UserGateway connect: {self.conn.url}"


class UserService:
    def __init__(self, user_gateway: UserGateway) -> None:
        self.user_gateway = user_gateway

    def say(self)->str:
        return f"UserService {self.user_gateway.hello_world()}"


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def settings_provide(self) -> Settings:
        return Settings(url="http://localhost:5432/user_db")

    url = provide(UserGatewayImpl, scope=Scope.REQUEST, provides=UserGateway)


class ServiceUserProvide(Provider):
    scope = Scope.REQUEST

    service = provide(UserService)

container = make_container(UserProvider(), ServiceUserProvide())

with container() as req:
    us = req.get(UserService)
    print(us.say())  # Output: UserService UserGateway connect: http://localhost:5432/user_db
