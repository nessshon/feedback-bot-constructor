from aiogram.types import (
    InlineKeyboardButton,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)

from ._init_value import InitValue
from ...utils.texts._language_code import LanguageCode


class ButtonCode(InitValue):
    back: str
    skip: str
    delete: str
    confirm: str

    create_bot: str
    bot_management: str
    bot_info: str
    bot_settings: str

    select_group: str

    user_list: str
    text_list: str

    startup: str
    shutdown: str

    set_group: str
    edit_group: str
    update_token: str

    edit_text_ru: str
    edit_text_en: str
    edit_media_url: str

    export_csv: str
    export_json: str


class TextButton:
    """
    Class representing a text message.
    """
    data = {
        LanguageCode.en: {
            ButtonCode.back: "↩️ Back",
            ButtonCode.skip: "⏭️ Skip",
            ButtonCode.delete: "🗑️ Delete",
            ButtonCode.confirm: "✅ Confirm",
            ButtonCode.create_bot: "🤖 Create a Bot",
            ButtonCode.bot_management: "⚙️ Bot Management",
            ButtonCode.select_group: "👥 Select Group",
            ButtonCode.user_list: "👤 Users",
            ButtonCode.text_list: "📜 Messages",
            ButtonCode.startup: "▶️ Enable",
            ButtonCode.shutdown: "⏹️ Shutdown",
            ButtonCode.set_group: "🔗 Connect Group",
            ButtonCode.edit_group: "✏️ Edit Group",
            ButtonCode.update_token: "🔄 Update TOKEN",
            ButtonCode.edit_text_ru: "🇷🇺 Edit in Russian",
            ButtonCode.edit_text_en: "🇬🇧 Edit in English",
            ButtonCode.edit_media_url: "🌐 Edit Banner Link",
            ButtonCode.export_csv: "💾 Export to CSV",
            ButtonCode.export_json: "📋 Export to JSON",
        },
        LanguageCode.ru: {
            ButtonCode.back: "↩️ Назад",
            ButtonCode.skip: "⏭️ Пропустить",
            ButtonCode.delete: "🗑️ Удалить",
            ButtonCode.confirm: "✅ Подтвердить",
            ButtonCode.create_bot: "🤖 Создать бота",
            ButtonCode.bot_management: "⚙️ Управление ботами",
            ButtonCode.select_group: "👥 Выбрать группу",
            ButtonCode.user_list: "👤 Пользователи",
            ButtonCode.text_list: "📜 Сообщения",
            ButtonCode.startup: "▶️ Включить",
            ButtonCode.shutdown: "⏹️ Выключить",
            ButtonCode.set_group: "🔗 Привязать группу",
            ButtonCode.edit_group: "✏️ Изменить группу",
            ButtonCode.update_token: "🔄 Обновить TOKEN",
            ButtonCode.edit_text_ru: "🇷🇺 Изменить на русском",
            ButtonCode.edit_text_en: "🇬🇧 Изменить на английском",
            ButtonCode.edit_media_url: "🌐 Изменить ссылку баннера",
            ButtonCode.export_csv: "💾 Экспорт в CSV",
            ButtonCode.export_json: "📋 Экспорт в JSON",
        }
    }

    def __init__(self, language_code: str) -> None:
        """
        Initialize the TextMessage object.

        :param language_code: The language code for the text message.
        """
        self.language_code = language_code

    def get(self, code: str) -> str:
        """
        Returns the text corresponding to the given code.

        :param code: The code for which the text is to be retrieved.
        :return: The text corresponding to the given code.
        """
        return self.data[self.language_code][code]

    def get_button(
            self,
            code: str,
            url: str | None = None,
            web_app: WebAppInfo | None = None,
            login_url: LoginUrl | None = None,
            switch_inline_query: str | None = None,
            switch_inline_query_current_chat: str | None = None,
            switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = None,
    ) -> InlineKeyboardButton:
        text = self.get(code)
        if url:
            return InlineKeyboardButton(text=text, url=url)
        elif web_app:
            return InlineKeyboardButton(text=text, web_app=web_app)
        elif login_url:
            return InlineKeyboardButton(text=text, login_url=login_url)
        elif switch_inline_query:
            return InlineKeyboardButton(text=text, switch_inline_query=switch_inline_query)
        elif switch_inline_query_current_chat:
            return InlineKeyboardButton(text=text, switch_inline_query_current_chat=switch_inline_query_current_chat)
        elif switch_inline_query_chosen_chat:
            return InlineKeyboardButton(text=text, switch_inline_query_chosen_chat=switch_inline_query_chosen_chat)
        return InlineKeyboardButton(text=text, callback_data=code)
