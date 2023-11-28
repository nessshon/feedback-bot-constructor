import asyncio
from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ErrorEvent
from aiogram.exceptions import TelegramBadRequest
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.bot_multi.filters import IsPrivateFilter
from app.bot_multi.texts import TextMessage, MessageCode
from app.bot_multi.types.album import Album
from app.bot_multi.utils import create_topic
from app.database.models import BotDB
from app.mongodb.models import UserMongo

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(Command("start"))
async def handler(message: Message, text_message: TextMessage) -> None:
    """
    Handle the /start command.
    """
    emoji = await message.answer("👋")
    await message.delete()
    await asyncio.sleep(1.8)

    text = text_message.get(MessageCode.welcome_message)
    await emoji.edit_text(text.format(name=message.from_user.full_name))


@router.message(F.media_group_id, flags={"throttling_key": "album"})
@router.message(F.media_group_id.is_(None))
async def handler(message: Message,
                  bot_db: BotDB,
                  user_mongo: UserMongo,
                  text_message: TextMessage,
                  mongodb: AsyncIOMotorDatabase,
                  album: Optional[Album] = None,
                  ) -> None:
    """
    Handle media messages in private chats.
    """
    if user_mongo.is_banned:
        """If user is banned ignore all messages."""
        return

    message_thread_id = user_mongo.message_thread_id

    async def copy_message_to_topic():
        if not album:
            await message.copy_to(
                chat_id=bot_db.group_id,
                message_thread_id=message_thread_id,
            )
        else:
            await album.copy_to(
                chat_id=bot_db.group_id,
                message_thread_id=message_thread_id,
            )

    try:
        await copy_message_to_topic()
    except TelegramBadRequest as ex:
        if "message thread not found" in ex.message:
            message_thread_id = await create_topic(
                bot=message.bot,
                mongodb=mongodb,
                user_mongo=user_mongo,
                group_id=bot_db.group_id,
            )
            await copy_message_to_topic()
        else:
            raise

    text = text_message.get(MessageCode.message_sent)
    msg = await message.reply(text)
    await asyncio.sleep(5)
    await msg.delete()


@router.edited_message()
async def handler(message: Message, text_message: TextMessage) -> None:
    """
    Handle edited messages in private chats.
    """
    text = text_message.get(MessageCode.message_edited)
    msg = await message.reply(text)
    await asyncio.sleep(5)
    await msg.delete()


@router.error(F.exception.message.contains("chat not found"))
async def handler(_: ErrorEvent) -> None:
    """
    Error handler for a router when a group chat is not found.

    :param _: The ErrorEvent object.
    """
