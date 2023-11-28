import typing as t
from dataclasses import dataclass, asdict
from motor.motor_asyncio import AsyncIOMotorDatabase

T = t.TypeVar("T", bound="AbstractModel")


@dataclass
class AbstractModel:
    _id: t.Optional[t.Any] = None

    @dataclass
    class Meta:
        collection: str

    @property
    def id(self) -> t.Any:
        return self._id

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    async def create(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            **kwargs,
    ) -> T:
        collection = mongodb[cls.Meta.collection]
        model = cls(**kwargs)
        await collection.insert_one(model.to_dict())
        return model

    @classmethod
    async def get(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            _id: t.Any,
    ) -> T | None:
        collection = mongodb[cls.Meta.collection]
        data = await collection.find_one({"_id": _id})
        return cls(**data) if data else None

    @classmethod
    async def get_by_key(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            key: str,
            value: t.Any,
    ) -> T | None:
        collection = mongodb[cls.Meta.collection]
        data = await collection.find_one({key: value})
        return cls(**data) if data else None

    @classmethod
    async def update(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            **kwargs,
    ) -> T | None:
        collection = mongodb[cls.Meta.collection]
        data = await collection.find_one_and_update({"_id": kwargs["_id"]}, {"$set": kwargs})
        return cls(**data) if data else None

    @classmethod
    async def delete(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            _id: t.Any,
    ) -> None:
        collection = mongodb[cls.Meta.collection]
        await collection.find_one_and_delete({"_id": _id})

    @classmethod
    async def all(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
    ) -> t.List[T]:
        collection = mongodb[cls.Meta.collection]
        return [cls(**data) async for data in collection.find()]

    @classmethod
    async def create_or_update(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            **kwargs,
    ) -> T:
        instance = await cls.update(mongodb, **kwargs)
        if instance is not None:
            return instance
        return await cls.create(mongodb, **kwargs)

    @classmethod
    async def paginate(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            page: int,
            page_size: int,
    ) -> t.List[T]:
        return await cls.paginate_by_filter(mongodb, page, page_size)

    @classmethod
    async def total_pages(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            page_size: int,
    ) -> int:
        collection = mongodb[cls.Meta.collection]
        total_docs = await collection.count_documents({})
        return (total_docs + page_size - 1) // page_size

    @classmethod
    async def paginate_by_filter(
            cls: t.Type[T],
            mongodb: AsyncIOMotorDatabase,
            page: int,
            page_size: int,
            **kwargs,
    ) -> t.List[T]:
        collection = mongodb[cls.Meta.collection]
        skip = (page - 1) * page_size
        cursor = collection.find(**kwargs).skip(skip).limit(page_size)
        return [cls(**data) async for data in cursor]
