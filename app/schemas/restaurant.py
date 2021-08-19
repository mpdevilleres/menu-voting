from typing import Optional

import datetime
import uuid

from pydantic import BaseModel


class RestaurantCreateSchema(BaseModel):
    name: str
    location: Optional[str]


class RestaurantResponseSchema(BaseModel):
    class Config:
        orm_mode = True

    id: uuid.UUID
    name: str
    location: Optional[str]
    date_added: datetime.datetime
    date_updated: datetime.datetime


class RestaurantListResponseSchema(BaseModel):
    items: list[RestaurantResponseSchema]
    total: int


class MenuCreateSchema(BaseModel):
    name: str
    date_served: datetime.datetime


class MenuResponseSchema(BaseModel):
    class Config:
        orm_mode = True

    id: uuid.UUID
    name: str
    restaurant_name: str
    date_served: datetime.date
    date_added: datetime.datetime
    date_updated: datetime.datetime


class MenuListResponseSchema(BaseModel):
    items: list[MenuResponseSchema]
    total: int
