from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from .config import ALLOWED_UPDATES, Config
from .database.models import Base, BotDB
from .bot_main import commands as main_commands
from .bot_multi import commands as multi_commands


# noinspection PyUnusedLocal
async def startup(
        bot: Bot,
        config: Config,
        session: AiohttpSession,
        engine: AsyncEngine,
        sessionmaker: async_sessionmaker,
) -> None:
    """
    Startup handler for the bot.
    """
    # Create database tables
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    # Setup commands for the main bot
    await main_commands.setup(bot)

    # Set webhook for the main bot
    path = config.webhook.PATH_BOT_MAIN.format(bot_token=config.bot.TOKEN)
    await bot.set_webhook(url=config.webhook.DOMAIN + path,
                          allowed_updates=ALLOWED_UPDATES)

    # Setup commands and set webhook for all active multi-bots
    async with sessionmaker() as async_session:
        for bot_db in await BotDB.all(async_session):
            if bot_db.is_active:
                try:
                    token = BotDB.decrypt_token(config.SECRET_KEY, bot_db.token)
                    multi_bot = Bot(token, session, ParseMode.HTML)
                    await multi_commands.setup(multi_bot)

                    path = config.webhook.PATH_BOT_MULTI.format(bot_token=token)
                    await multi_bot.set_webhook(url=config.webhook.DOMAIN + path,
                                                allowed_updates=ALLOWED_UPDATES)
                except TelegramUnauthorizedError:
                    # Handle unauthorized errors
                    pass


# noinspection PyUnusedLocal
async def shutdown(
        bot: Bot,
        config: Config,
        session: AiohttpSession,
        engine: AsyncEngine,
        sessionmaker: async_sessionmaker,
) -> None:
    """
    Shutdown handler for the bot.
    """
    # Delete commands and webhook for all active multi-bots
    async with sessionmaker() as async_session:
        for bot_db in await BotDB.all(async_session):
            if bot_db.is_active:
                try:
                    token = BotDB.decrypt_token(config.SECRET_KEY, bot_db.token)
                    multi_bot = Bot(token, session, ParseMode.HTML)
                    await multi_commands.delete(multi_bot)

                    await multi_bot.delete_webhook()
                except TelegramUnauthorizedError:
                    # Handle unauthorized errors
                    pass

    # Delete commands and webhook for the main bot
    await main_commands.delete(bot)
    await bot.delete_webhook()

    # Close session and all database connections
    await session.close()
    await engine.dispose()
