from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
)


async def setup(bot: Bot) -> None:
    """
    Setup bot commands.

    :param bot: The Bot object.
    """
    commands = {
        "en": [
            BotCommand(command="start", description="Restart bot"),
        ],
        "ru": [
            BotCommand(command="start", description="Перезапустить бота"),
        ]
    }

    # Set commands for all private chats in Russian language
    await bot.set_my_commands(
        commands=commands["ru"],
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru"
    )
    # Set commands for all private chats in English language
    await bot.set_my_commands(
        commands=commands["en"],
        scope=BotCommandScopeAllPrivateChats(),
    )


async def delete(bot: Bot) -> None:
    """
    Delete bot commands.

    :param bot: The Bot object.
    """
    # Delete commands for all private chats in any language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
    )
    # Delete commands for all private chats in Russian language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru",
    )
