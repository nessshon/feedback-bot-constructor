from __future__ import annotations

import typing as t

from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from ._base import Base

T = t.TypeVar("T", bound="AbstractModel")


class AbstractModel(Base):
    """Base class for all models."""

    __abstract__ = True
    __allow_unmapped__ = True

    @staticmethod
    def _get_column(
            model: t.Type[T],
            col: InstrumentedAttribute[t.Any],
    ) -> str:
        """Get the name of a column in a model."""
        name = col.name
        if name not in model.__table__.columns:
            raise ValueError(f"Column {name} not found in {model.__name__}")
        return name

    @classmethod
    def _get_primary_key(cls) -> str:
        """Return the primary key of the model."""
        return cls.__table__.primary_key.columns.values()[0].name

    @classmethod
    async def create(
            cls: t.Type[T],
            async_session: AsyncSession,
            **kwargs,
    ) -> T:
        """Create a new record in the database."""
        instance = cls(**kwargs)
        async_session.add(instance)
        await async_session.commit()
        await async_session.refresh(instance)
        return instance

    @classmethod
    async def get(
            cls: t.Type[T],
            async_session: AsyncSession,
            primary_key: int,
    ) -> T:
        """Get a record from the database by its primary key."""
        return await async_session.get(cls, primary_key)

    @classmethod
    async def get_by_key(
            cls: t.Type[T],
            async_session: AsyncSession,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
    ) -> T | None:
        """Get a record by a key."""
        statement = select(cls).filter_by(**{cls._get_column(cls, key): value})
        result = await async_session.execute(statement)
        return result.scalars().first()

    @classmethod
    async def update(
            cls: t.Type[T],
            async_session: AsyncSession,
            primary_key: int,
            **kwargs,
    ) -> None:
        """Update a record in the database by its primary key."""
        instance = await cls.get(async_session, primary_key)
        if instance:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            await async_session.commit()

    @classmethod
    async def update_by_key(
            cls: t.Type[T],
            async_session: AsyncSession,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
            **kwargs,
    ) -> None:
        """Update a record in the database by a key."""
        instance = await cls.get_by_key(async_session, key, value)
        if instance:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            await async_session.commit()

    @classmethod
    async def delete(
            cls: t.Type[T],
            async_session: AsyncSession,
            primary_key: int,
    ) -> None:
        """Delete a record from the database by its primary key."""
        instance = await cls.get(async_session, primary_key)
        if instance:
            await async_session.delete(instance)
            await async_session.commit()

    @classmethod
    async def delete_by_key(
            cls: t.Type[T],
            async_session: AsyncSession,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
    ) -> None:
        """Delete a record from the database by a key."""
        instance = await cls.get_by_key(async_session, key, value)
        if instance:
            await async_session.delete(instance)
            await async_session.commit()

    @classmethod
    async def create_or_update(
            cls: t.Type[T],
            async_session: AsyncSession,
            **kwargs,
    ) -> T:
        """Get and update a record from the database by its primary key."""
        primary_key = kwargs.get(cls._get_primary_key())
        instance = await cls.get(async_session, primary_key)
        if instance:
            await cls.update(async_session, primary_key, **kwargs)
            return instance
        return await cls.create(async_session, **kwargs)

    @classmethod
    async def exists(
            cls: t.Type[T],
            async_session: AsyncSession,
            primary_key: int,
    ) -> bool:
        """Check if a record exists in the database by its primary key."""
        return await async_session.get(cls, primary_key) is not None

    @classmethod
    async def exists_by_filter(
            cls: t.Type[T],
            async_session: AsyncSession,
            **kwargs,
    ) -> bool:
        """Check if a record exists in the database by a filter."""
        statement = select(cls).filter_by(**kwargs)
        result = await async_session.execute(statement)
        return bool(result.scalar())

    @classmethod
    async def paginate(
            cls: t.Type[T],
            async_session: AsyncSession,
            page_number: int,
            page_size: int,
    ) -> t.Sequence[T]:
        """Get paginated records from the database."""
        statement = select(cls).limit(page_size).offset((page_number - 1) * page_size)
        result = await async_session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def paginate_by_filter(
            cls: t.Type[T],
            async_session: AsyncSession,
            page_number: int,
            page_size: int,
            **kwargs,
    ) -> t.Sequence[T]:
        """Get paginated records from the database by a filter."""
        statement = select(cls).filter_by(**kwargs).limit(page_size).offset((page_number - 1) * page_size)
        result = await async_session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def total_pages(
            cls: t.Type[T],
            async_session: AsyncSession,
            page_size: int,
    ) -> int:
        statement = select(func.count(cls.__table__.primary_key.columns[0]))
        query = await async_session.execute(statement)
        return (query.scalar() + page_size - 1) // page_size

    @classmethod
    async def all(
            cls: t.Type[T],
            async_session: AsyncSession,
    ) -> t.Sequence[T]:
        """Get all records from the database."""
        statement = select(cls)
        result = await async_session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def all_by_filter(
            cls: t.Type[T],
            async_session: AsyncSession,
            **kwargs,
    ) -> t.Sequence[T]:
        """Get all records from the database by a filter."""
        statement = select(cls).filter_by(**kwargs)
        result = await async_session.execute(statement)
        return result.scalars().all()
