import asyncio
import random

import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import (
    BaseModel,
    async_session,
    engine,
)
from app.factory.restaurant import (
    MenuFactory,
    RestaurantFactory,
)
from app.factory.user import UserFactory
from app.models.restaurant import (
    Menu,
    Restaurant,
)
from app.models.user import (
    User,
    UserType,
)
from app.server import create_app


@pytest.fixture(scope="session")
def event_loop():
    yield asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
        yield


@pytest.fixture
async def db_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@pytest.fixture
async def restaurant(db_session) -> Restaurant:
    restaurant = RestaurantFactory.create()
    db_session.add(restaurant)
    await db_session.commit()

    yield restaurant

    await db_session.delete(restaurant)
    await db_session.commit()


@pytest.fixture
async def restaurants(db_session) -> list[Restaurant]:
    restaurants = []
    fake = Faker()
    for _ in range(100):
        d = fake.date_time_between(start_date="-7d", end_date="now")
        restaurant = RestaurantFactory.create(date_added=d, date_updated=d)
        restaurants.append(restaurant)
        db_session.add(restaurant)
    await db_session.commit()

    yield restaurants

    for restaurant in restaurants:
        await db_session.delete(restaurant)
    await db_session.commit()


@pytest.fixture
async def menu(db_session, restaurant) -> Menu:
    fake = Faker()
    d = fake.date_time_between(start_date="-7d", end_date="now")
    menu = MenuFactory.create(
        date_added=d,
        date_updated=d,
        date_served=fake.date_time_between(start_date="-7d", end_date="now"),
        restaurant_id=restaurant.id,
    )
    db_session.add(menu)
    await db_session.commit()

    yield menu

    await db_session.delete(menu)
    await db_session.commit()


@pytest.fixture
async def menus(db_session, restaurant) -> list[Menu]:
    menus = []
    fake = Faker()
    for _ in range(100):
        d = fake.date_time_between(start_date="-7d", end_date="now")
        menu = MenuFactory.create(
            date_added=d,
            date_updated=d,
            date_served=fake.date_time_between(
                start_date="-7d", end_date="now"
            ),
            restaurant_id=restaurant.id,
        )
        menus.append(menu)
        db_session.add(menu)
    await db_session.commit()

    yield menus

    for menu in menus:
        await db_session.delete(menu)
    await db_session.commit()


@pytest.fixture
async def user_employee(db_session) -> User:
    user = UserFactory.create(user_type=UserType.EMPLOYEE)
    db_session.add(user)
    await db_session.commit()

    yield user

    await db_session.delete(user)
    await db_session.commit()


@pytest.fixture
async def user_restaurant(db_session) -> User:
    user = UserFactory.create(user_type=UserType.RESTAURANT)
    db_session.add(user)
    await db_session.commit()

    yield user

    await db_session.delete(user)
    await db_session.commit()


@pytest.fixture
async def client_restaurant(user_restaurant) -> AsyncClient:
    _app = create_app()
    access_token = user_restaurant.create_access_token(60)
    headers = {
        "authorization": f"bearer {access_token}",
        "x-build-version": str(random.uniform(2.0, 3.0)),
    }

    async with AsyncClient(
        app=_app, base_url="http://test", headers=headers
    ) as _client:  # noqa
        yield _client


@pytest.fixture
async def client_employee(user_employee) -> AsyncClient:
    _app = create_app()
    access_token = user_employee.create_access_token(60)
    headers = {
        "authorization": f"bearer {access_token}",
        "x-build-version": str(random.uniform(2.0, 3.0)),
    }

    async with AsyncClient(
        app=_app, base_url="http://test", headers=headers
    ) as _client:  # noqa
        yield _client


@pytest.fixture
async def client() -> AsyncClient:
    _app = create_app()
    headers = {"x-build-version": str(random.uniform(2.0, 3.0))}
    async with AsyncClient(
        app=_app, base_url="http://test", headers=headers
    ) as _client:  # noqa
        yield _client
