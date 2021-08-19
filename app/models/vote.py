from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

from app import (
    db,
    settings,
)


class Vote(db.BaseModel):
    __table_args__ = (
        UniqueConstraint("menu_id", "user_id", "date_voted", name="uq_vote"),
    )
    menu_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f"{settings.BACKEND_DATABASE_SCHEMA}.menu.id"),
    )
    user_id = Column(
        UUID(), ForeignKey(f"{settings.BACKEND_DATABASE_SCHEMA}.user.id")
    )
    point = Column(Integer, nullable=False)
    date_voted = Column(Date)
