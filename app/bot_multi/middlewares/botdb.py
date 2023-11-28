from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BotDB


class BotDBMiddleware(BaseMiddleware):
    """
    Middleware for retrieving the BotDB object based on the bot ID.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Call the middleware.

        :param handler: The handler function.
        :param event: The Telegram event.
        :param data: Additional data.
        """
        bot: Bot = data["bot"]
        async_session: AsyncSession = data["async_session"]

        bot_user = await bot.get_me()
        bot_db = await BotDB.get(async_session, bot_user.id)

        # Pass the bot_db to the handler function
        data["bot_db"] = bot_db

        # Call the handler function with the event and data
        return await handler(event, data)
