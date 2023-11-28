from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatMemberUpdated
from aiogram.utils.link import create_tg_link
from aiogram.utils.markdown import hlink
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.bot_multi.filters import IsPrivateFilter
from app.bot_multi.texts import TextMessage, MessageCode
from app.bot_multi.utils import create_topic
from app.database.models.bot import BotDB
from app.mongodb.models import UserMongo

router = Router()


@router.my_chat_member(IsPrivateFilter())
async def handler(update: ChatMemberUpdated,
                  bot_db: BotDB,
                  user_mongo: UserMongo,
                  text_message: TextMessage,
                  mongodb: AsyncIOMotorDatabase,
                  ) -> None:
    """
    Handle updates to the chat member status in a private chat.

    :param update: The ChatMemberUpdated object.
    :param bot_db: The BotDB object.
    :param user_mongo: The UserMongo object.
    :param text_message: The TextMessage object.
    :param mongodb: The AsyncIOMotorDatabase object for the UserMongo collection.
    """
    state = update.new_chat_member.status
    await UserMongo.update(mongodb, _id=user_mongo.id, state=state)

    message_thread_id = user_mongo.message_thread_id

    if state == ChatMemberStatus.MEMBER:
        text = text_message.get(MessageCode.user_started_bot)
    else:
        text = text_message.get(MessageCode.user_stopped_bot)

    url = create_tg_link("user", id=user_mongo.id)
    name = hlink(user_mongo.full_name, url=url)

    try:
        await update.bot.send_message(
            chat_id=bot_db.group_id,
            text=text.format(name=name),
            message_thread_id=message_thread_id,
        )
    except TelegramBadRequest as ex:
        if "message thread not found" in ex.message:
            message_thread_id = await create_topic(
                bot=update.bot,
                mongodb=mongodb,
                user_mongo=user_mongo,
                group_id=bot_db.group_id,
            )
            await update.bot.send_message(
                chat_id=bot_db.group_id,
                text=text.format(name=name),
                message_thread_id=message_thread_id,
            )
