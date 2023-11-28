from aiogram.utils.markdown import hide_link

from app.mongodb.models import TextMongo

__all__ = [
    "LanguageCode",
    "MessageCode",
    "TextMessage",

    "default_mongodb_texts",
]


class InitVal:
    """
    Base class for initializing class attributes with their names as values.
    """

    def __init_subclass__(cls, **kwargs):
        """
        Initialize subclass attributes with their names as values.

        :param kwargs: Keyword arguments representing the subclass attributes.
        """
        for attr in cls.__annotations__:
            setattr(cls, attr, attr)
        super().__init_subclass__(**kwargs)


class LanguageCode(InitVal):
    """
    Class representing language codes.

    Attributes:
        ru (str): Language code for Russian.
        en (str): Language code for English.
    """
    ru: str
    en: str


class MessageCode(InitVal):
    """
    Class representing Message codes.
    """
    user_started_bot: str
    user_stopped_bot: str
    source: str
    user_blocked: str
    user_unblocked: str
    blocked_by_user: str
    user_information: str
    message_not_sent: str
    message_sent_to_user: str
    silent_mode_enabled: str
    silent_mode_disabled: str

    welcome_message: str
    message_sent: str
    message_edited: str


class TextMessage:
    """
    Class for managing text messages in different languages.
    """
    data: dict = {
        LanguageCode.en: {
            MessageCode.user_started_bot: (
                "<b>User {name} stated bot!</b>\n\n"
                "<b>List of available commands:</b>\n\n"
                "• /ban\n"
                "Block/Unblock user\n"
                "<code>Block the user if you do not want to receive messages from him.</code>\n\n"
                "• /silent\n"
                "Activate/Deactivate silent mode\n"
                "<code>When silent mode is enabled, messages are not sent to the user.</code>\n\n"
                "• /information\n"
                "User information\n"
                "<code>Receive a message with basic information about the user.</code>"
            ),
            MessageCode.user_stopped_bot: (
                "<b>User {name} stopped the bot!</b>"
            ),
            MessageCode.source: (
                "Source code available at "
                "<a href=\"https://github.com/nessshon/feedback-topics-bot\">GitHub</a>"
            ),
            MessageCode.user_blocked: (
                "<b>User blocked!</b>\n\n"
                "Messages from the user are not accepted."
            ),
            MessageCode.user_unblocked: (
                "<b>User unblocked!</b>\n\n"
                "Messages from the user are being accepted again."
            ),
            MessageCode.blocked_by_user: (
                "<b>Message not sent!</b>\n\n"
                "The bot has been blocked by the user."
            ),
            MessageCode.user_information: (
                "<b>ID:</b>\n"
                "- <code>{id}</code>\n"
                "<b>Name:</b>\n"
                "- {full_name}\n"
                "<b>Status:</b>\n"
                "- {state}\n"
                "<b>Username:</b>\n"
                "- {username}\n"
                "<b>Blocked:</b>\n"
                "- {is_blocked}\n"
                "<b>Registration date:</b>\n"
                "- {created_at}\n"
            ),
            MessageCode.message_not_sent: (
                "<b>Message not sent!</b>\n\n"
                "An unexpected error occurred."
            ),
            MessageCode.message_sent_to_user: (
                "<b>Message sent to user!</b>"
            ),
            MessageCode.silent_mode_enabled: (
                "<b>Silent mode activated!</b>\n\n"
                "Messages will not be delivered to the user."
            ),
            MessageCode.silent_mode_disabled: (
                "<b>Silent mode deactivated!</b>\n\n"
                "The user will receive all messages."
            )
        },
        LanguageCode.ru: {
            MessageCode.user_started_bot: (
                "<b>Пользователь {name} запустил(а) бота!</b>\n\n"
                "<b>Список доступных команд:</b>\n\n"
                "• /ban\n"
                "Заблокировать/Разблокировать пользователя\n"
                "<code>Заблокируйте пользователя, если не хотите получать от него сообщения.</code>\n\n"
                "• /silent\n"
                "Активировать/Деактивировать тихий режим\n"
                "<code>При включенном тихом режиме сообщения не отправляются пользователю.</code>\n\n"
                "• /information\n"
                "Информация о пользователе\n"
                "<code>Получить сообщение с основной информацией о пользователе.</code>"
            ),
            MessageCode.user_stopped_bot: (
                "<b>Пользователь {name} остановил(а) бота!</b>"
            ),
            MessageCode.source: (
                "Исходный код доступен на "
                "<a href=\"https://github.com/nessshon/feedback-topics-bot\">GitHub</a>"
            ),
            MessageCode.user_blocked: (
                "<b>Пользователь заблокирован!</b>\n\n"
                "Сообщения от пользователя не принимаются."
            ),
            MessageCode.user_unblocked: (
                "<b>Пользователь разблокирован!</b>\n\n"
                "Сообщения от пользователя вновь принимаются."
            ),
            MessageCode.blocked_by_user: (
                "<b>Сообщение не отправлено!</b>\n\n"
                "Бот был заблокирован пользователем."
            ),
            MessageCode.user_information: (
                "<b>ID:</b>\n"
                "- <code>{id}</code>\n"
                "<b>Имя:</b>\n"
                "- {full_name}\n"
                "<b>Статус:</b>\n"
                "- {state}\n"
                "<b>Username:</b>\n"
                "- {username}\n"
                "<b>Заблокирован:</b>\n"
                "- {is_blocked}\n"
                "<b>Дата регистрации:</b>\n"
                "- {created_at}\n"
            ),
            MessageCode.message_not_sent: (
                "<b>Сообщение не отправлено!</b>\n\n"
                "Произошла неожиданная ошибка."
            ),
            MessageCode.message_sent_to_user: (
                "<b>Сообщение отправлено пользователю!</b>"
            ),
            MessageCode.silent_mode_enabled: (
                "<b>Тихий режим активирован!</b>\n\n"
                "Сообщения не будут доставлены пользователю."
            ),
            MessageCode.silent_mode_disabled: (
                "<b>Тихий режим деактивирован!</b>\n\n"
                "Пользователь будет получать все сообщения."
            )
        },
    }

    def __init__(self, language_code: str) -> None:
        """
        Initialize the TextMessage class.

        :param language_code: The language code for the messages.
        """
        if language_code in [LanguageCode.ru, LanguageCode.en]:
            self.language_code = language_code
        else:
            self.language_code = LanguageCode.en

    def insert_mongodb_text(self, texts: list[TextMongo]) -> None:
        """
        Insert text_list from MongoDB into the message dictionary.
        """
        for text in texts:
            if text.media_url:
                text.en = hide_link(text.media_url) + text.en
                text.ru = hide_link(text.media_url) + text.ru
            self.data[LanguageCode.en][text.code] = text.en
            self.data[LanguageCode.ru][text.code] = text.ru

    def get(self, code: str) -> str:
        """
        Get the message for the given code in the selected language.

        :param code: The code of the message.
        :return: The message string.
        """
        return self.data[self.language_code][code]


# Default text_list to insert into MongoDB.
# Placed separately for dynamic and editable text_list.
default_mongodb_texts: list[TextMongo] = [
    TextMongo(
        code="welcome_message",
        en=(
            "Hello, <b>{name}!</b>\n\n"
            "Write your question, and we will answer you as soon as possible:"
        ),
        ru=(
            "Привет, <b>{name}!</b>\n\n"
            "<b>Напишите ваш вопрос и мы ответим вам в ближайшее время:</b>"
        ),
        media_url="https://telegra.ph//file/e17f59a066f95a686b2ac.jpg",
        description_en="Welcome message",
        description_ru="Приветственное сообщение",
    ),
    TextMongo(
        code="message_sent",
        en=(
            "<b>Message sent!</b>\n\n"
            "Expect a response."
        ),
        ru=(
            "<b>Сообщение отправлено!</b>\n\n"
            "Ожидайте ответа."
        ),
        media_url="https://telegra.ph//file/bf1a949406367748d205c.jpg",
        description_en="User message sent",
        description_ru="Сообщение пользователя отправлено",
    ),
    TextMongo(
        code="message_edited",
        en=(
            "<b>The message was edited only in your chat.</b>\n\n"
            "To send an edited message, send it as a new message."
        ),
        ru=(
            "<b>Сообщение отредактировано только в вашем чате.</b>\n\n"
            "Чтобы отправить отредактированное сообщение, отправьте его как новое сообщение."
        ),
        media_url="https://telegra.ph//file/b346594181006adab79eb.jpg",
        description_en="User message modified",
        description_ru="Сообщение пользователя изменено.",
    ),
]
