from aiogram import Router, Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import CallbackQuery

from app.bot_main.utils.texts.buttons import ButtonCode
from app.bot_main.utils.manager import Manager
from app.bot_main.utils.filters import IsPrivateFilter
from app.bot_main.utils.states import State
from app.config import ALLOWED_UPDATES
from app.database.models import BotDB
from app.mongodb.models import TextMongo

from .windows import Window
from ...utils.texts.messages import MessageCode

router = Router()
router.callback_query.filter(IsPrivateFilter())


@router.callback_query(State.main_menu)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.create_bot:
            await Window.create_bot(manager)
        case ButtonCode.bot_management:
            await Window.bot_list(manager)
    await call.answer()


@router.callback_query(State.create_bot)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.main_menu(manager)
    await call.answer()


@router.callback_query(State.select_group)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.create_bot(manager)
    await call.answer()


@router.callback_query(State.bot_list)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await manager.state.update_data(current_page=1)
            await Window.main_menu(manager)
        case bot_id if bot_id.isdigit():
            await manager.state.update_data(bot_id=int(bot_id))
            await Window.bot_info(manager)
        case cdata if cdata.startswith("page:"):
            page = int(cdata.split(":")[1])
            await manager.state.update_data(current_page=page)
            await Window.bot_list(manager)
    await call.answer()


@router.callback_query(State.bot_info)
async def handler(call: CallbackQuery, manager: Manager, session: AiohttpSession) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.bot_list(manager)
        case ButtonCode.user_list:
            await Window.user_list(manager)
        case ButtonCode.text_list:
            await Window.text_list(manager)
        case ButtonCode.back:
            await Window.bot_info(manager)
        case ButtonCode.update_token:
            text = manager.text_message.get(MessageCode.in_development)
            await call.answer(text, show_alert=True)
        case ButtonCode.delete:
            text = manager.text_message.get(MessageCode.in_development)
            await call.answer(text, show_alert=True)
        case action if action in [ButtonCode.shutdown, ButtonCode.startup]:
            state_data = await manager.state.get_data()
            bot_db = await BotDB.get(manager.async_session, state_data["bot_id"])
            token = BotDB.decrypt_token(manager.config.SECRET_KEY, bot_db.token)
            bot = Bot(token=token, session=session)
            if action == ButtonCode.shutdown:
                await bot.delete_webhook(drop_pending_updates=True)
                is_active = False
            else:
                path = manager.config.webhook.PATH_BOT_MULTI.format(bot_token=token)
                await bot.set_webhook(url=manager.config.webhook.DOMAIN + path,
                                      allowed_updates=ALLOWED_UPDATES,
                                      drop_pending_updates=True)
                is_active = True
            await BotDB.update(manager.async_session, bot_db.id, is_active=is_active)
            await Window.bot_info(manager)
        case action if action in [ButtonCode.set_group, ButtonCode.edit_group]:
            await Window.select_group(manager)
    await call.answer()


@router.callback_query(State.user_list)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await manager.state.update_data(current_page=1)
            await Window.bot_info(manager)
        case export_type if export_type in [ButtonCode.export_csv, ButtonCode.export_json]:
            text = manager.text_message.get(MessageCode.in_development)
            await call.answer(text, show_alert=True)
        case user_id if user_id.isdigit():
            await manager.state.update_data(user_id=int(user_id))
            await Window.user_info(manager)
        case cdata if cdata.startswith("page:"):
            page = int(cdata.split(":")[1])
            await manager.state.update_data(current_page=page)
            await Window.user_list(manager)
    await call.answer()


@router.callback_query(State.user_info)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.user_list(manager)
    await call.answer()


@router.callback_query(State.text_list)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await manager.state.update_data(current_page=1)
            await Window.bot_info(manager)
        case text_id if text_id.isdigit():
            await manager.state.update_data(text_id=int(text_id))
            await Window.text_info(manager)
        case cdata if cdata.startswith("page:"):
            page = int(cdata.split(":")[1])
            await manager.state.update_data(current_page=page)
            await Window.text_list(manager)
    await call.answer()


@router.callback_query(State.text_info)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.text_list(manager)
        case lang_code if lang_code in [ButtonCode.edit_text_ru, ButtonCode.edit_text_en]:
            await manager.state.update_data(text_language_code=lang_code[-2:])
            await Window.text_edit_text(manager)
        case ButtonCode.edit_media_url:
            await Window.text_edit_media(manager)
    await call.answer()


@router.callback_query(State.text_edit_text)
@router.callback_query(State.text_edit_media)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.text_info(manager)
    await call.answer()


@router.callback_query(State.text_edit_text_confirm)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.text_edit_text(manager)
        case ButtonCode.confirm:
            state_data = await manager.state.get_data()
            bot = await BotDB.get(manager.async_session, state_data["bot_id"])
            text_language_code = state_data["text_language_code"]
            text_id = state_data["text_id"]
            await TextMongo.update(
                manager.mongo_client[bot.username],
                _id=text_id,
                **{text_language_code: state_data["text"]},
            )
            await Window.text_info(manager)
    await call.answer()


@router.callback_query(State.text_edit_media_confirm)
async def handler(call: CallbackQuery, manager: Manager) -> None:
    match call.data:
        case ButtonCode.back:
            await Window.text_edit_media(manager)
        case ButtonCode.confirm:
            state_data = await manager.state.get_data()
            bot = await BotDB.get(manager.async_session, state_data["bot_id"])
            text_id = state_data["text_id"]
            await TextMongo.update(
                manager.mongo_client[bot.username],
                _id=text_id,
                media_url=state_data["media_url"],
            )
            await Window.text_info(manager)
    await call.answer()
