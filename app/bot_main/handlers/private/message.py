from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User
from aiogram.utils.token import validate_token, TokenValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot_main.utils.manager import Manager
from app.bot_main.utils.states import State
from app.bot_main.utils.filters import IsPrivateFilter
from app.config import Config, ALLOWED_UPDATES
from app.database.models import BotDB, UserDB

from .windows import Window
from ...utils import is_valid_url

router = Router()
router.message.filter(IsPrivateFilter())


@router.message(Command("start"))
async def handler(message: Message, manager: Manager) -> None:
    await Window.main_menu(manager)
    await message.delete()


@router.message(F.text, State.create_bot)
async def handler(message: Message,
                  state: FSMContext,
                  async_session: AsyncSession,
                  config: Config,
                  manager: Manager,
                  user_db: UserDB,
                  ) -> None:
    try:
        token = message.text
        validate_token(token)
        bot: Bot = Bot(message.text, message.bot.session, ParseMode.HTML)
        bot_user: User = await bot.get_me()

        await BotDB.create(
            async_session,
            id=bot_user.id,
            user_id=user_db.id,
            token=BotDB.encrypt_token(config.SECRET_KEY, token),
            username=bot_user.username,
        )
        await bot.set_webhook(
            config.webhook.DOMAIN +
            config.webhook.PATH_BOT_MULTI.format(bot_token=token),
            allowed_updates=ALLOWED_UPDATES,
        )

        await state.update_data(created_bot=bot_user.model_dump(exclude_none=True))
        await Window.select_group(manager)

    except TokenValidationError:
        ...

    await message.delete()


@router.message(State.text_edit_text)
async def handler(message: Message, manager: Manager) -> None:
    if message.content_type == "text" and len(message.text) <= 1500:
        await manager.state.update_data(text=message.text)
        await Window.text_edit_text_confirm(manager)
    await manager.delete_message(message)


@router.message(State.text_edit_media)
async def handler(message: Message, manager: Manager) -> None:
    if message.content_type == "text" and len(message.text) <= 500:
        if is_valid_url(message.text):
            await manager.state.update_data(media_url=message.text)
            await Window.text_edit_media_confirm(manager)
    await manager.delete_message(message)
