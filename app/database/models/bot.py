from datetime import datetime

from cryptography.fernet import Fernet
from sqlalchemy import *

from ._abc import AbstractModel


class BotDB(AbstractModel):
    """
    Represents a bot in the database.

    Attributes:
          id (int): The unique identifier of the bot.
          user_id (int): The ID of the user who owns the bot.
          group_id (int): The ID of the group where the bot is located.
          token (str): The bot token, BotFather provides.
          username (str): The bot username.
          is_active (bool): Whether the bot is active.
          created_at (datetime): The timestamp when the user was created.
    """
    __tablename__ = "bots"

    id: int = Column(
        BigInteger,
        primary_key=True,
    )
    user_id: int = Column(
        BigInteger,
        ForeignKey(
            "user_list.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    group_id: int = Column(
        BigInteger,
        nullable=True,
    )
    token: str = Column(
        VARCHAR(length=250),
        nullable=False,
    )
    username: str = Column(
        VARCHAR(length=64),
        nullable=True,
    )
    is_active: bool = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    created_at: datetime = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    @staticmethod
    def encrypt_token(secret_key: str, token: str) -> str:
        """
        Encrypts the given Bot TOKEN using the provided encryption key.

        :param secret_key: The encryption key used to encrypt the TOKEN.
        :param token: The secret to be encrypted.
        :return: The encrypted TOKEN.
        """
        cipher_suite = Fernet(secret_key.encode())
        encrypted_key = cipher_suite.encrypt(token.encode())

        return encrypted_key.decode()

    @staticmethod
    def decrypt_token(secret_key: str, encrypted_token: str) -> str:
        """
        Decrypts the given encrypted key using the provided key.

        :param secret_key: The key used to decrypt the encrypted key.
        :param encrypted_token: The encrypted TOKEN to be decrypted.
        :return: The decrypted TOKEN as a string.
        """
        cipher_suite = Fernet(secret_key.encode())
        decrypted_key = cipher_suite.decrypt(encrypted_token.encode())

        return decrypted_key.decode()
