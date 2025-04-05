from dishka import make_async_container

from src.infrastructure.provide import AppProvider
from src.settings import Settings, settings

container = make_async_container(AppProvider(), context={Settings: settings})
