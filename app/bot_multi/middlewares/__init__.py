from aiogram import Dispatcher

from .album import AlbumMiddleware
from .botdb import BotDBMiddleware
from .config import ConfigMiddleware
from .database import DBSessionMiddleware
from .usermongo import UserMongoMiddleware
from .messages import TextMessageMiddleware
from .mongodb import MongoDBMiddleware
from .throttling import ThrottlingMiddleware


def bot_multi_middlewares_register(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.

    :param dp: The Dispatcher object.
    :param kwargs: Additional keyword arguments.
    """
    dp.update.outer_middleware.register(DBSessionMiddleware(kwargs["sessionmaker"]))
    dp.update.outer_middleware.register(ConfigMiddleware(kwargs["config"]))
    dp.update.outer_middleware.register(BotDBMiddleware())
    dp.update.outer_middleware.register(MongoDBMiddleware(kwargs["mongo_client"]))

    dp.update.outer_middleware.register(TextMessageMiddleware())
    dp.update.outer_middleware.register(UserMongoMiddleware())

    dp.message.outer_middleware.register(ThrottlingMiddleware(album=.01))
    dp.message.outer_middleware.register(AlbumMiddleware())


__all__ = [
    "bot_multi_middlewares_register",
]
