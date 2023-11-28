import logging
import traceback
from asyncio import sleep

from aiogram import Bot, Dispatcher, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, BufferedInputFile
from aiogram.utils.markdown import hcode, hbold
from aiogram.exceptions import TelegramBadRequest

from app.config import Config


async def errors(event: ErrorEvent, bot: Bot, config: Config) -> None:
    """
    Error handler for all Telegram Bot API errors.

    :param event: The ErrorEvent object.
    :param bot: The Bot object.
    :param config: The Config object.
    """
    logging.exception(f'Update: {event.update}\nException: {event.exception}')

    try:
        document_message = await bot.send_document(
            chat_id=config.bot.DEV_ID,
            document=BufferedInputFile(
                traceback.format_exc().encode(),
                filename=f'error_{event.update.update_id}.txt',
            ),
            caption=f'{hbold(type(event.exception).__name__)}: {str(event.exception)[:1021]}...',
        )

        update_json = event.update.model_dump_json(indent=2, exclude_none=True)
        for chunk in [update_json[i:i + 4096] for i in range(0, len(update_json), 4096)]:
            await sleep(.2)
            await document_message.reply(text=hcode(chunk))

    except TelegramBadRequest:
        pass


def register_errors_handlers(dp: Dispatcher) -> None:
    """
    Register error handlers for bots.

    :param dp: The Dispatcher object.
    """
    dp.error.register(
        ExceptionTypeFilter(TelegramBadRequest),
        F.exception.message.contains("message"),
    )
    dp.error.register(errors)
