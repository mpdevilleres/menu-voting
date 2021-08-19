import datetime
import enum

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import (
    Column,
    Text,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import validates

from app import (
    db,
    settings,
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@enum.unique
class UserType(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    RESTAURANT = "RESTAURANT"


class User(db.BaseModel):
    name = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    user_type = Column(
        ENUM(UserType), nullable=False, default=UserType.EMPLOYEE
    )

    @validates("password")
    def generate_hash_password(self, _, value: str):
        return pwd_context.hash(value)

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.password)

    def create_access_token(
        self, expires_delta: int = None, additional_data: dict = None
    ):
        if expires_delta:
            expires_delta = datetime.timedelta(minutes=expires_delta)
        else:
            expires_delta = datetime.timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {
            "sub": self.username,
            "exp": datetime.datetime.utcnow() + expires_delta,
        }
        if additional_data:
            to_encode.update(additional_data)

        return jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
