from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID

from app import (
    db,
    settings,
)


class Restaurant(db.BaseModel):
    name = Column(Text, nullable=False, unique=True)
    location = Column(Text, nullable=True)


class Menu(db.BaseModel):
    name = Column(Text, nullable=False, unique=True)
    date_served = Column(Date)
    restaurant_id = Column(
        UUID(), ForeignKey(f"{settings.BACKEND_DATABASE_SCHEMA}.restaurant.id")
    )
