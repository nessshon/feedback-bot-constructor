from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
    setup_application,
)
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .bot_main import (
    bot_main_include_routers,
    bot_main_middlewares_register,
)
from .bot_multi import (
    bot_multi_include_routers,
    bot_multi_middlewares_register,
)
from .config import load_config
from .logger import setup_logger
from .on import startup, shutdown


def main():
    """
    Main entry point of the application.
    """
    # Load configuration
    config = load_config()

    # Create Aiohttp session
    session = AiohttpSession()

    # Create MongoDB client
    mongo = AsyncIOMotorClient(config.mongodb.dsn())

    # Create database engine
    engine = create_async_engine(
        url=config.database.url(),
        pool_pre_ping=True,
    )
    # Create session maker for database
    sessionmaker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create Redis storage
    storage = RedisStorage.from_url(
        url=config.redis.dsn(),
        key_builder=DefaultKeyBuilder(with_bot_id=True),
    )

    # Bot settings
    bot_settings = {
        "session": session,
        "parse_mode": ParseMode.HTML,
    }
    # Dispatcher settings
    dispatcher_settings = {
        "config": config,
        "session": session,
        "engine": engine,
        "sessionmaker": sessionmaker,
        "mongo_client": mongo,
        "storage": storage,
    }

    # Create web application
    app = web.Application()

    # Create main bot and dispatcher
    bot_main = Bot(token=config.bot.TOKEN, **bot_settings)
    bot_main_dispatcher = Dispatcher(**dispatcher_settings)
    # Include routers and register middlewares for main bot
    bot_main_include_routers(bot_main_dispatcher)
    bot_main_middlewares_register(
        bot_main_dispatcher,
        config=config,
        sessionmaker=sessionmaker,
    )

    # Create multi-bot dispatcher with main bot as default bot
    bot_multi_dispatcher = Dispatcher(
        **dispatcher_settings,
        dp_main=bot_main_dispatcher,
        bot_main=bot_main,
    )
    # Include routers and register middlewares for multi-bot dispatcher
    bot_multi_include_routers(bot_multi_dispatcher)
    bot_multi_middlewares_register(
        bot_multi_dispatcher,
        config=config,
        mongo_client=mongo,
        sessionmaker=sessionmaker,
    )

    # Register startup and shutdown functions for main dispatcher
    bot_main_dispatcher.startup.register(startup)
    bot_main_dispatcher.shutdown.register(shutdown)

    # Register SimpleRequestHandler for main bot
    bot_main_path = config.webhook.PATH_BOT_MAIN.format(bot_token=config.bot.TOKEN)
    SimpleRequestHandler(
        dispatcher=bot_main_dispatcher,
        bot=bot_main,
    ).register(app, path=bot_main_path)

    # Register TokenBasedRequestHandler for multi-bot dispatcher
    bot_multi_path = config.webhook.PATH_BOT_MULTI
    TokenBasedRequestHandler(
        dispatcher=bot_multi_dispatcher,
        bot_settings=bot_settings,
    ).register(app, path=bot_multi_path)

    # Setup application with main and multi-bot dispatchers
    setup_application(app, bot_main_dispatcher, bot=bot_main)
    setup_application(app, bot_multi_dispatcher)

    # Run the web application
    web.run_app(app, host=config.app.HOST, port=config.app.PORT)


if __name__ == "__main__":
    # Setup logger
    setup_logger()

    # Run the main function
    main()
