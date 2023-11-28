import asyncio

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import User, ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot_main.utils.texts.buttons import TextButton
from app.bot_main.utils.texts.messages import MessageCode, TextMessage
from app.bot_main.utils import keyboards
from app.bot_main.utils.keyboards import InlineKeyboardPaginator
from app.bot_main.utils.manager import Manager
from app.bot_main.utils.states import State
from app.database.models import BotDB
from app.mongodb.models import UserMongo, TextMongo


class Window:

    @staticmethod
    async def main_menu(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.main_menu)
        reply_markup = keyboards.main_menu(manager.text_button).as_markup()

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.main_menu)

    @staticmethod
    async def create_bot(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.send_token)
        reply_markup = keyboards.back(manager.text_button).as_markup()

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.create_bot)

    @staticmethod
    async def select_group(manager: Manager) -> None:
        state_data = await manager.state.get_data()
        bot: User = User(**state_data["created_bot"])

        text = manager.text_message.get(MessageCode.select_group)
        reply_markup = keyboards.select_group(manager.text_button, bot.username).as_markup()

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.select_group)

    @staticmethod
    async def bot_list(manager: Manager) -> None:
        state_data = await manager.state.get_data()
        current_page, page_size = state_data.get("current_page", 1), 10

        bots_list = await BotDB.paginate(manager.async_session, current_page, page_size)
        total_pages = await BotDB.total_pages(manager.async_session, page_size)
        items = [(bot.username, bot.id) for bot in bots_list]

        text = manager.text_message.get(MessageCode.bot_list)
        after_builder = keyboards.back(manager.text_button)
        reply_markup = InlineKeyboardPaginator(
            items=items,
            current_page=current_page,
            total_pages=total_pages,
            after_builder=after_builder,
        ).as_markup()

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.bot_list)

    @staticmethod
    async def bot_info(manager: Manager) -> None:
        state_data = await manager.state.get_data()
        bot_db = await BotDB.get(manager.async_session, state_data["bot_id"])

        text = manager.text_message.get(MessageCode.bot_info)
        reply_markup = keyboards.bot_information(manager.text_button, bot_db).as_markup()

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.bot_info)

    @staticmethod
    async def user_list(manager: Manager) -> None:
        state_data = await manager.state.get_data()
        current_page, page_size = state_data.get("current_page", 1), 10

        bot_db = await BotDB.get(manager.async_session, state_data["bot_id"])
        users_list = await UserMongo.paginate(manager.mongo_client[bot_db.username], current_page, page_size)
        total_pages = await UserMongo.total_pages(manager.mongo_client[bot_db.username], page_size)
        items = [(user.full_name, user.id) for user in users_list]

        text = manager.text_message.get(MessageCode.user_list)
        before_builder = keyboards.export_tools(manager.text_button)
        after_builder = keyboards.back(manager.text_button)
        reply_markup = InlineKeyboardPaginator(
            items=items,
            current_page=current_page,
            total_pages=total_pages,
            before_builder=before_builder,
            after_builder=after_builder,
        ).as_markup()

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.user_list)

    @staticmethod
    async def user_info(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.user_info)
        reply_keyboard = keyboards.back(manager.text_button).as_markup()

        await manager.send_message(text, reply_markup=reply_keyboard)
        await manager.state.set_state(State.user_info)

    @staticmethod
    async def text_list(manager: Manager) -> None:
        state_data = await manager.state.get_data()
        current_page, page_size = state_data.get("current_page", 1), 10

        bot_db = await BotDB.get(manager.async_session, state_data["bot_id"])
        text_list = await TextMongo.paginate(manager.mongo_client[bot_db.username], current_page, page_size)
        total_pages = await TextMongo.total_pages(manager.mongo_client[bot_db.username], page_size)
        items = [(getattr(text, f"description_{manager.user.language_code}"), text.id)
                 for text in text_list]

        text = manager.text_message.get(MessageCode.text_list)
        after_builder = keyboards.back(manager.text_button)
        reply_markup = InlineKeyboardPaginator(
            items=items,
            current_page=current_page,
            total_pages=total_pages,
            after_builder=after_builder,
        ).as_markup()

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.text_list)

    @staticmethod
    async def text_info(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.text_info)
        reply_keyboard = keyboards.text_info(manager.text_button).as_markup()

        await manager.send_message(text, reply_markup=reply_keyboard)
        await manager.state.set_state(State.text_info)

    @staticmethod
    async def text_edit_text(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.text_edit_text)
        reply_keyboard = keyboards.back(manager.text_button).as_markup()

        state_data = await manager.state.get_data()
        bot_db = await BotDB.get(manager.async_session, state_data["bot_id"])
        text_mongo = await TextMongo.get(manager.mongo_client[bot_db.username], state_data["text_id"])
        frmt = {"old_text": getattr(text_mongo, state_data["text_language_code"][-2:])}

        await manager.send_message(text.format_map(frmt), reply_markup=reply_keyboard)
        await manager.state.set_state(State.text_edit_text)

    @staticmethod
    async def text_edit_text_confirm(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.text_edit_text_confirm)
        reply_keyboard = keyboards.back_confirm(manager.text_button).as_markup()

        state_data = await manager.state.get_data()
        frmt = {"new_text": state_data["text"]}

        await manager.send_message(text.format_map(frmt), reply_markup=reply_keyboard)
        await manager.state.set_state(State.text_edit_text_confirm)

    @staticmethod
    async def text_edit_media(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.text_edit_media)
        reply_keyboard = keyboards.back(manager.text_button).as_markup()

        state_data = await manager.state.get_data()
        bot_db = await BotDB.get(manager.async_session, state_data["bot_id"])
        text_mongo = await TextMongo.get(manager.mongo_client[bot_db.username], state_data["text_id"])
        frmt = {"old_media_url": text_mongo.media_url}

        await manager.send_message(text.format_map(frmt), reply_markup=reply_keyboard)
        await manager.state.set_state(State.text_edit_media)

    @staticmethod
    async def text_edit_media_confirm(manager: Manager) -> None:
        text = manager.text_message.get(MessageCode.text_edit_media_confirm)
        reply_keyboard = keyboards.back_confirm(manager.text_button).as_markup()

        state_data = await manager.state.get_data()
        frmt = {"new_media_url": state_data["media_url"]}

        await manager.send_message(text.format_map(frmt), reply_markup=reply_keyboard)
        await manager.state.set_state(State.text_edit_media_confirm)


class CustomManager(Manager):
    def __init__(self, bot: Bot, state: FSMContext, user: User) -> None:
        super().__init__(
            emoji="🤖",
            data={
                "bot": bot,
                "state": state,
                "event_from_user": user,
            },
        )


async def manage_group_window(
        bot: Bot,
        user: User,
        state: FSMContext,
        update: ChatMemberUpdated,
        async_session: AsyncSession,
        bot_db: BotDB,
) -> None:
    manager = CustomManager(bot, state, user)
    text_buttons = TextButton(user.language_code)
    text = TextMessage(user.language_code).get(MessageCode.bot_info)
    reply_markup = keyboards.bot_information(text_buttons, bot_db).as_markup()

    await manager.send_message(text, reply_markup=reply_markup)
    await state.set_state(State.bot_info)
    await asyncio.sleep(1)

    try:
        frmt = {
            "bot_username": bot_db.username,
            "group_title": update.chat.title,
        }
        if update.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            text = TextMessage(user.language_code).get(MessageCode.group_connected)
            group_id = update.chat.id
        elif update.new_chat_member.status == ChatMemberStatus.MEMBER:
            text = TextMessage(user.language_code).get(MessageCode.group_waiting)
            group_id = None
        else:
            text = TextMessage(user.language_code).get(MessageCode.group_disconnected)
            group_id = None

        await BotDB.update(async_session, bot_db.id, group_id=group_id)
        msg = await bot.send_message(user.id, text=text.format_map(frmt))
        await asyncio.sleep(10)
        await msg.delete()

    except TelegramBadRequest as ex:
        if "chat not found" not in ex.message:
            raise
