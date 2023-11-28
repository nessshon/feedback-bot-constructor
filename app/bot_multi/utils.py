from aiogram import Bot
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BotDB
from app.mongodb.models import UserMongo


async def delete_bot_dependencies(bot_db: BotDB,
                                  async_session: AsyncSession,
                                  mongodb: AsyncIOMotorClient,
                                  ) -> None:
    """
    Delete dependencies associated with a bot.
    """
    await mongodb.drop_database(bot_db.username)
    await BotDB.delete(async_session, bot_db.id)


async def create_topic(bot: Bot,
                       mongodb: AsyncIOMotorDatabase,
                       user_mongo: UserMongo,
                       group_id: int
                       ) -> int:
    """
    Create a forum topic and update the user's message_thread_id.
    """
    topic = await bot.create_forum_topic(
        chat_id=group_id,
        name=user_mongo.full_name,
        icon_custom_emoji_id="5417915203100613993",
    )
    await UserMongo.update(
        mongodb,
        _id=user_mongo.id,
        message_thread_id=topic.message_thread_id,
    )
    return topic.message_thread_id
