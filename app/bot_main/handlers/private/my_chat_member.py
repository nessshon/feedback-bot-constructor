from aiogram import Router
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot_main.utils.filters import IsPrivateFilter
from app.database.models import UserDB

router = Router()


@router.my_chat_member(IsPrivateFilter())
async def handler(update: ChatMemberUpdated,
                  async_session: AsyncSession,
                  user_db: UserDB,
                  ) -> None:
    """
    Handle updates of the bot chat member status.

    :param update: The chat member update event.
    :param async_session: The asynchronous SQLAlchemy session.
    :param user_db: The user object from database.
    :return: None
    """
    await UserDB.update(async_session, user_db.id, state=update.new_chat_member.status)
