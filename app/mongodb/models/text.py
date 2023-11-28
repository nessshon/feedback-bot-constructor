from __future__ import annotations

import typing as t
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorDatabase

from ._abc import AbstractModel


@dataclass
class TextMongo(AbstractModel):
    """
    Model for storing text messages in MongoDB.

    Attributes:
        _id (str): The unique identifier for the text.
        code (str): The unique code for the text.
        en (str): The text in English.
        ru (str): The text in Russian.
        media_url (str): The URL of the media.
        description_en (str): The description in English.
        description_ru (str): The description in Russian.
    """
    en: t.Optional[str] = None
    ru: t.Optional[str] = None
    code: t.Optional[str] = None
    _id: t.Optional[int] = None
    media_url: t.Optional[str] = None
    description_en: t.Optional[str] = None
    description_ru: t.Optional[str] = None

    @dataclass
    class Meta:
        collection = "texts"

    @classmethod
    async def insert_default(
            cls: TextMongo,
            mongodb: AsyncIOMotorDatabase,
            texts: t.List[TextMongo],
    ) -> None:
        collection = mongodb[cls.Meta.collection]
        for _id, text in enumerate(texts, start=1):
            text._id = _id
            await collection.insert_one(text.to_dict())
