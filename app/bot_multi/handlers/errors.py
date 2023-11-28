from aiogram import Dispatcher, F
from aiogram.exceptions import (
    TelegramUnauthorizedError,
    TelegramBadRequest,
)
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent


async def unauthorized(_: ErrorEvent) -> bool:
    """
    Error handler for TelegramUnauthorizedError.

    :param _: The ErrorEvent object.
    """


def register_errors_handlers(dp: Dispatcher) -> None:
    """
    Register error handlers for bots.

    :param dp: The Dispatcher object.
    """
    dp.error.register(
        unauthorized,
        ExceptionTypeFilter(TelegramUnauthorizedError),
    )
    dp.error.register(
        ExceptionTypeFilter(TelegramBadRequest),
        F.exception.message.contains("message"),
    )
