from aiogram import Dispatcher

from . import group
from . import private
from .errors import register_errors_handlers


def bot_multi_include_routers(dp: Dispatcher) -> None:
    """
    Include bot routers.

    :param dp: The Dispatcher object.
    """
    dp.include_routers(
        *[
            group.message.router,
            group.my_chat_member.router,

            private.message.router,
            private.my_chat_member.router,
        ]
    )
    register_errors_handlers(dp)


__all__ = [
    "bot_multi_include_routers",
]
