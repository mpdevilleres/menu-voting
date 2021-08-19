from typing import Optional

import datetime
import uuid

from pydantic import BaseModel

from app.models.user import UserType


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserCreateSchema(BaseModel):
    name: Optional[str]
    username: str
    password: str
    user_type: UserType = UserType.EMPLOYEE


class UserResponseSchema(BaseModel):
    class Config:
        orm_mode = True

    id: uuid.UUID
    name: str
    username: str
    user_type: UserType
    date_added: datetime.datetime
    date_updated: datetime.datetime
