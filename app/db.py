import datetime

from sqlalchemy import (
    Column,
    DateTime,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    sessionmaker,
)

from app import settings

engine = create_async_engine(settings.POSTGRES_DATABASE_URI, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class BaseBackend:
    @declared_attr
    def __tablename__(cls):  # noqa
        return cls.__name__.lower()

    __table_args__ = {"schema": settings.BACKEND_DATABASE_SCHEMA}

    id = Column(
        UUID(), primary_key=True, server_default=text("gen_random_uuid()")
    )
    date_added = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow
    )
    date_updated = Column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


BaseModel = declarative_base(cls=BaseBackend)
