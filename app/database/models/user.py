from datetime import datetime

from sqlalchemy import *

from ._abc import AbstractModel


class UserDB(AbstractModel):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user.
        state (str): The state of the user (e.g. "member", "kicked").
        full_name (str): The full name of the user.
        username (str): The username of the user.
        created_at (datetime): The timestamp when the user was created.
    """
    __tablename__ = "user_list"

    id: int = Column(
        BigInteger,
        primary_key=True,
    )
    state: str = Column(
        VARCHAR(length=6),
        nullable=False,
        default="member",
    )
    full_name: str = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    username: str = Column(
        VARCHAR(length=64),
        nullable=True,
    )
    created_at: datetime = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
