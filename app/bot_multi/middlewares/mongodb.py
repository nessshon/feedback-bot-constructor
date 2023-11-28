from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from motor.motor_asyncio import AsyncIOMotorClient

from app.database.models import BotDB


class MongoDBMiddleware(BaseMiddleware):
    """
    Middleware for managing MongoDB.
    """

    def __init__(self, mongo_client: AsyncIOMotorClient) -> None:
        """
        Initialize the MongoDBMiddleware.

        :param mongo_client: The MongoDB client.
        """
        self.mongo_client = mongo_client

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
        bot_db: BotDB = data["bot_db"]

        database = self.mongo_client.get_database(bot_db.username)
        data["mongodb"] = database

        # Call the handler function with the event and data
        return await handler(event, data)
