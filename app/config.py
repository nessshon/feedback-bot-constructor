from dataclasses import dataclass
from pathlib import Path

from aiogram.enums import UpdateType
from environs import Env

BASE_DIR = Path(__file__).resolve().parent

ALLOWED_UPDATES = [
    UpdateType.MESSAGE,
    UpdateType.CALLBACK_QUERY,
    UpdateType.MY_CHAT_MEMBER,
    UpdateType.EDITED_MESSAGE,
]


@dataclass
class BotConfig:
    TOKEN: str
    DEV_ID: int


@dataclass
class AppConfig:
    HOST: str
    PORT: int


@dataclass
class WebhookConfig:
    DOMAIN: str
    PATH_BOT_MAIN: str
    PATH_BOT_MULTI: str


@dataclass
class MongoDBConfig:
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str

    def dsn(self) -> str:
        """
        Generates a MongoDB connection DSN (Data Source Name) using the provided host, port, username, and password.

        :return: The generated MongoDB connection DSN.
        """
        return f"mongodb://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}"


@dataclass
class RedisConfig:
    HOST: str
    PORT: int
    DB: int

    def dsn(self) -> str:
        """
        Generates a Redis connection DSN (Data Source Name) using the provided host, port, and database.

        :return: The generated DSN.
        """
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


@dataclass
class DatabaseConfig:
    USERNAME: str
    PASSWORD: str
    DATABASE: str
    HOST: str
    PORT: int

    def url(self, driver: str = "mysql+aiomysql") -> str:
        """
        Generates a database connection URL using the provided driver, username, password, host, port, and database.

        :param driver: The driver to use for the connection. Defaults to "mysql+aiomysql".
        :return: The generated connection URL.
        """
        return f"{driver}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


@dataclass
class Config:
    bot: BotConfig
    app: AppConfig
    webhook: WebhookConfig
    mongodb: MongoDBConfig
    redis: RedisConfig
    database: DatabaseConfig

    SECRET_KEY: str


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        SECRET_KEY=env.str("SECRET_KEY"),

        bot=BotConfig(
            TOKEN=env.str("BOT_TOKEN"),
            DEV_ID=env.int("BOT_DEV_ID"),
        ),
        app=AppConfig(
            HOST=env.str("APP_HOST"),
            PORT=env.int("APP_PORT"),
        ),
        webhook=WebhookConfig(
            DOMAIN=env.str("WEBHOOK_DOMAIN"),
            PATH_BOT_MAIN=env.str("WEBHOOK_PATH_BOT_MAIN"),
            PATH_BOT_MULTI=env.str("WEBHOOK_PATH_BOT_MULTI"),
        ),
        mongodb=MongoDBConfig(
            HOST=env.str("MONGO_HOST"),
            PORT=env.int("MONGO_PORT"),
            USER=env.str("MONGO_USER"),
            PASSWORD=env.str("MONGO_PASSWORD"),
        ),
        redis=RedisConfig(
            HOST=env.str("REDIS_HOST"),
            PORT=env.int("REDIS_PORT"),
            DB=env.int("REDIS_DB"),
        ),
        database=DatabaseConfig(
            HOST=env.str("DB_HOST"),
            PORT=env.int("DB_PORT"),
            USERNAME=env.str("DB_USERNAME"),
            PASSWORD=env.str("DB_PASSWORD"),
            DATABASE=env.str("DB_DATABASE"),
        ),
    )
