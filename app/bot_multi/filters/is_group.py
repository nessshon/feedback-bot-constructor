from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Chat

from app.database.models import BotDB


class IsGroupFilter(BaseFilter):
    """
    Filter for checking if a message is in a group chat.
    """

    async def __call__(self, event: TelegramObject, event_chat: Chat) -> bool:
        """
        Call the filter.

        :param event: The event object (e.g., Message) to check.
        :param event_chat: The chat object associated with the event.
        :return: True if the message is in a group chat, False otherwise.
        """
        return event_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]


class IsGroupLinkedFilter(BaseFilter):
    """
    Filter for checking if a message is in a specific group chat.
    """

    async def __call__(self, event: TelegramObject, event_chat: Chat, bot_db: BotDB) -> bool:
        """
        Call the filter.

        :param event: The event object (e.g., Message) to check.
        :param event_chat: The chat object associated with the event.
        :return: True if the message is in a group chat, False otherwise.
        """
        return event_chat.id == bot_db.group_id
