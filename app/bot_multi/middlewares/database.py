from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DBSessionMiddleware(BaseMiddleware):
    """
    Middleware for handling database sessions.
    """

    def __init__(self, sessionmaker: async_sessionmaker):
        """
        Initialize the DBSessionMiddleware.

        :param sessionmaker: The async sessionmaker object for creating database sessions.
        """
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Call the middleware.

        :param handler: The handler function.
        :param event: The Telegram event.
        :param data: Additional data.
        """
        # Create a new session using the sessionmaker
        async with self.sessionmaker() as async_session:
            # Pass the async_session to the handler function
            data["async_session"] = async_session

            # Call the handler function with the event and data
            return await handler(event, data)
