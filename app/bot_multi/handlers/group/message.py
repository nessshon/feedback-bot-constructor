import asyncio
from contextlib import suppress
from typing import Optional

from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hcode
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.bot_multi.filters import IsGroupFilter
from app.bot_multi.filters.is_group import IsGroupLinkedFilter
from app.bot_multi.texts import TextMessage, MessageCode
from app.bot_multi.types.album import Album
from app.mongodb.models import UserMongo

router = Router()
router.message.filter(
    IsGroupFilter(),
    IsGroupLinkedFilter(),
    F.message_thread_id.is_not(None),
)


@router.message(Command("silent"))
async def handler(message: Message,
                  user_mongo: UserMongo,
                  text_message: TextMessage,
                  mongodb: AsyncIOMotorDatabase,
                  ) -> None:
    """
    Handle the /silent command.
    """
    if user_mongo.message_silent_mode:
        text = text_message.get(MessageCode.silent_mode_disabled)
        with suppress(TelegramBadRequest):
            await message.reply(text)
            await message.bot.unpin_chat_message(
                chat_id=message.chat.id,
                message_id=user_mongo.message_silent_id
            )
        user_mongo.message_silent_mode = False
        user_mongo.message_silent_id = None
    else:
        text = text_message.get(MessageCode.silent_mode_enabled)
        with suppress(TelegramBadRequest):
            msg = await message.reply(text)
            await msg.pin(disable_notification=True)
        user_mongo.message_silent_mode = True
        user_mongo.message_silent_id = msg.message_id

    await UserMongo.update(mongodb, **user_mongo.to_dict())


@router.message(Command("information"))
async def handler(message: Message,
                  user_mongo: UserMongo,
                  text_message: TextMessage,
                  ) -> None:
    """
    Handle the /information command.
    """
    true = "Да" if text_message.language_code == "ru" else "Yes"
    false = "Нет" if text_message.language_code == "ru" else "No"
    member = "Участник" if text_message.language_code == "ru" else user_mongo.state.title()
    kicked = "Покинул" if text_message.language_code == "ru" else user_mongo.state.title()

    frmt = {
        "id": user_mongo.id,
        "full_name": hcode(user_mongo.full_name),
        "state": member if user_mongo.state == "member" else kicked,
        "username": f"@{user_mongo.username}" if user_mongo.username else "-",
        "is_blocked": true if user_mongo.is_banned else false,
        "created_at": user_mongo.created_at.strftime("%Y-%m-%d %H:%M")
    }

    text = text_message.get(MessageCode.user_information)
    await message.reply(text.format(**frmt))


@router.message(Command(commands=["ban"]))
async def handler(message: Message,
                  user_mongo: UserMongo,
                  text_message: TextMessage,
                  mongodb: AsyncIOMotorDatabase,
                  ) -> None:
    """
    Handle the /ban command.
    """
    if user_mongo.is_banned:
        user_mongo.is_banned = False
        text = text_message.get(MessageCode.user_unblocked)
    else:
        user_mongo.is_banned = True
        text = text_message.get(MessageCode.user_blocked)
    await UserMongo.update(mongodb, **user_mongo.to_dict())
    await message.reply(text)


@router.message(
    F.pinned_message |
    F.forum_topic_edited |
    F.forum_topic_closed |
    F.forum_topic_reopened
)
async def handler(message: Message) -> None:
    """
    Delete the specified message.
    """
    await message.delete()


@router.message(F.media_group_id, F.from_user[F.is_bot.is_(False)], flags={"throttling_key": "album"})
@router.message(F.media_group_id.is_(None), F.from_user[F.is_bot.is_(False)])
async def handler(message: Message,
                  user_mongo: UserMongo,
                  text_message: TextMessage,
                  album: Optional[Album] = None,
                  ) -> None:
    """
    Handle all messages from user_list in group chats.
    """
    if user_mongo.message_silent_mode:
        """If silent mode is enabled ignore all messages"""
        return

    text = text_message.get(MessageCode.message_sent_to_user)

    try:
        if not album:
            await message.copy_to(chat_id=user_mongo.id)
        else:
            await album.copy_to(chat_id=user_mongo.id)
    except TelegramAPIError as ex:
        if "blocked" in ex.message:
            text = text_message.get(MessageCode.blocked_by_user)
    except (Exception,):
        text = text_message.get(MessageCode.message_not_sent)

    msg = await message.reply(text)
    await asyncio.sleep(5)
    await msg.delete()
