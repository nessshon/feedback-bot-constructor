from aiogram import Dispatcher

from . import private
from .error import register_errors_handlers


def bot_main_include_routers(dp: Dispatcher) -> None:
    """
    Include bot routers.
    """
    dp.include_routers(
        *[
            private.callback_query.router,
            private.message.router,
            private.my_chat_member.router,
        ]
    )
    register_errors_handlers(dp)


__all__ = [
    "bot_main_include_routers",
]
