from aiogram import Router, Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated, User
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot_multi.filters import IsGroupFilter
from app.database.models import BotDB

router = Router()
router.my_chat_member.filter(
    IsGroupFilter(),
    F.new_chat_member.status.in_(
        [
            ChatMemberStatus.KICKED,
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
        ]
    ),
    F.new_chat_member.user.is_bot.is_(True),
)


@router.my_chat_member()
async def handler(update: ChatMemberUpdated,
                  dp_main: Dispatcher,
                  bot_main: Bot,
                  async_session: AsyncSession,
                  ) -> None:
    """
    Handle updates to the chat member status in a group chat.
    """
    bot_user: User = update.new_chat_member.user
    bot_db = await BotDB.get(async_session, bot_user.id)

    creator_id = bot_db.user_id
    state = dp_main.fsm.resolve_context(bot_main, creator_id, creator_id)
    creator = await bot_main.get_chat_member(creator_id, creator_id)

    from app.bot_main.handlers.private.windows import manage_group_window
    await manage_group_window(bot_main, creator.user, state, update, async_session, bot_db)
