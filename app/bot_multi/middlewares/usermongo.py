from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import TelegramObject, User, Chat
from aiogram.utils.link import create_tg_link
from aiogram.utils.markdown import hlink
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.bot_multi.utils import create_topic
from app.mongodb.models import UserMongo


class UserMongoMiddleware(BaseMiddleware):
    """
    Middleware for creating an update and passing a user object from MongoDB.
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
        mongodb: AsyncIOMotorDatabase = data.get("mongodb")
        user: User = data.get("event_from_user")
        chat: Chat = data.get("event_chat")

        # Check if the chat type is not private
        if chat.type != ChatType.PRIVATE:
            if not data.get("event_thread_id", None):
                # It is assumed that if there is no topic ID, so we return.
                return await handler(event, data)
            # Get the user by message_thread_id
            user_mongo = await UserMongo.get_by_key(mongodb, "message_thread_id", data["event_thread_id"])
            # If the user is not in mongodb, then the topic does not apply to user_list, do nothing
            if not user_mongo: return  # noqa:E701

        else:
            # If chat type is PRIVATE, create or update the user by his User object.
            user_mongo = await UserMongo.create_or_update(
                mongodb,
                _id=user.id,
                username=user.username,
                full_name=user.full_name,
                language_code=user.language_code,
            )

        if not user_mongo.message_thread_id:
            # If the message_thread_id is None, then create a new topic and update it for the user.
            await self.create_first_topic(data, user_mongo, mongodb)

        # Pass the config data to the handler function
        data["user_mongo"] = user_mongo

        # Call the handler function with the event and data
        return await handler(event, data)

    @staticmethod
    async def create_first_topic(
            data: Dict[str, Any],
            user_mongo: UserMongo,
            mongodb: AsyncIOMotorDatabase,
    ) -> None:
        """
        Create the first topic for the user and send a message in the bot group.

        :param data: Additional data.
        :param user_mongo: The UserMongo object.
        :param mongodb: The MongoDB collection.
        """
        bot, bot_db = data["bot"], data["bot_db"]
        message_thread_id = await create_topic(bot, mongodb, user_mongo, bot_db.group_id)
        user_mongo.message_thread_id = message_thread_id

        text = data["text_message"].get("user_started_bot")
        url = create_tg_link("user", id=user_mongo.id)
        name = hlink(user_mongo.full_name, url=url)

        await bot.send_message(
            chat_id=bot_db.group_id,
            text=text.format(name=name),
            message_thread_id=message_thread_id,
        )
