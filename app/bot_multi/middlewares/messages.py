from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.bot_multi.texts import TextMessage, default_mongodb_texts
from app.mongodb.models import TextMongo


class TextMessageMiddleware(BaseMiddleware):
    """
    Middleware for passing text message data.
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
        mongodb: AsyncIOMotorDatabase = data.get("mongodb", None)
        user: User = data.get("event_from_user", None)

        if mongodb is not None and user is not None:
            # Retrieve text messages from MongoDB
            texts = await TextMongo.all(mongodb)

            if not texts:
                # Insert default text messages if none exist
                await TextMongo.insert_default(mongodb, default_mongodb_texts)
                texts = await TextMongo.all(mongodb)

            # Create TextMessage object with user's language code
            text_message = TextMessage(user.language_code)
            text_message.insert_mongodb_text(texts)

            # Store text_message in data dictionary
            data["text_message"] = text_message

        # Call the handler function with the event and data
        return await handler(event, data)
