from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
)


async def setup(bot: Bot) -> None:
    """
    Setup bot commands.

    :param bot: The Bot object.
    """
    commands = {
        "en": [
            BotCommand(command="start", description="Restart"),
        ],
        "ru": [
            BotCommand(command="start", description="Перезапустить"),
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

    group_commands = {
        "en": [
            BotCommand(command="ban", description="Block/Unblock a user"),
            BotCommand(command="silent", description="Activate/Deactivate silent Mode"),
            BotCommand(command="information", description="User information"),
        ],
        "ru": [
            BotCommand(command="ban", description="Заблокировать/Разблокировать пользователя"),
            BotCommand(command="silent", description="Активировать/Деактивировать тихий режим"),
            BotCommand(command="information", description="Информация о пользователе"),
        ]
    }

    # Set commands for all group chats in Russian language
    await bot.set_my_commands(
        commands=group_commands["ru"],
        scope=BotCommandScopeAllGroupChats(),
        language_code="ru"
    )
    # Set commands for all group chats in English language
    await bot.set_my_commands(
        commands=group_commands["en"],
        scope=BotCommandScopeAllGroupChats(),
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
    # Delete commands for all group chats in any language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllGroupChats(),
    )
    # Delete commands for all group chats in Russian language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllGroupChats(),
        language_code="ru",
    )
