from aiogram import Dispatcher

from .config import ConfigMiddleware
from .database import DBSessionMiddleware
from .manager import ManagerMiddleware
from .throttling import ThrottlingMiddleware


def bot_main_middlewares_register(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.

    :param dp: The Dispatcher object.
    :param kwargs: Additional keyword arguments.
    """
    dp.update.middleware.register(DBSessionMiddleware(kwargs["sessionmaker"]))
    dp.update.middleware.register(ConfigMiddleware(kwargs["config"]))
    dp.update.middleware.register(ThrottlingMiddleware())
    dp.update.middleware.register(ManagerMiddleware())


__all__ = [
    "bot_main_middlewares_register",
]
