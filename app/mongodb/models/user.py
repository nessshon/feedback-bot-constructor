from __future__ import annotations

import typing as t
from dataclasses import field, dataclass
from datetime import datetime

from ._abc import AbstractModel


@dataclass
class UserMongo(AbstractModel):
    """
    Model for storing user_list in MongoDB.

    Attributes:
        _id (int): The unique identifier for the user.
        username (str): The username of the user.
        full_name (str): The full name of the user.
        state (str): The state of the user (e.g. "member", "kicked").
        is_banned (bool): Whether the user is banned or not.
        message_silent_mode (bool): Whether the user is in silent mode or not.
        message_silent_id (int): The ID of the message in silent mode.
        message_thread_id (int): The ID of the message thread.
        created_at (datetime): The timestamp when the user was created.
    """
    _id: t.Optional[int] = None
    username: t.Optional[str] = None
    full_name: t.Optional[str] = None
    language_code: t.Optional[str] = None
    state: t.Optional[str] = "member"
    is_banned: t.Optional[bool] = False
    message_silent_mode: t.Optional[bool] = False
    message_silent_id: t.Optional[int] = None
    message_thread_id: t.Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @dataclass
    class Meta:
        collection = "users"
