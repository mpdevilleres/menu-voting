from typing import Optional

from uuid import UUID

from pydantic import BaseModel
from pydantic.types import conint


class VoteSchema(BaseModel):
    menu_id: UUID
    point: Optional[conint(ge=1, le=3)]


class VoteResponseSchema(BaseModel):
    class Config:
        orm_mode = True

    id: UUID
    menu_id: UUID
    user_id: UUID
    point: Optional[int]


class VoteV2CreateSchema(BaseModel):
    votes: list[VoteSchema]


class VoteV2ResponseSchema(BaseModel):
    votes: list[VoteResponseSchema]


# TODO this is deprecated
class VoteV1CreateSchema(BaseModel):
    menu_id: UUID


# TODO this is deprecated
class VoteV1ResponseSchema(BaseModel):
    class Config:
        orm_mode = True

    id: UUID
    menu_id: UUID
    user_id: UUID
