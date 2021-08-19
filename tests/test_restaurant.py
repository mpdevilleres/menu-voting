import datetime
import uuid

import pytest
from sqlalchemy import select

from app.models.restaurant import (
    Menu,
    Restaurant,
)


@pytest.mark.asyncio
async def test_restaurant_retrieve(client_restaurant, db_session, restaurants):
    response = await client_restaurant.get("/api/v1/restaurants")
    assert response.status_code == 200
    payload = response.json()
    assert payload.keys() == {"items", "total"}

    actual_dates = [r["date_added"] for r in payload["items"]]
    expected_dates = [
        r.date_added.astimezone(datetime.timezone.utc).isoformat()
        for r in restaurants
    ]
    assert actual_dates != expected_dates
    assert actual_dates == sorted(expected_dates, reverse=True)


@pytest.mark.asyncio
async def test_restaurant_create(client_restaurant, db_session):
    response = await client_restaurant.post(
        "/api/v1/restaurants",
        json={"name": uuid.uuid4().hex, "location": "AUH"},
    )
    assert response.status_code == 201
    payload = response.json()

    result = await db_session.execute(
        select(Restaurant).where(Restaurant.id == payload["id"])
    )
    restaurant = result.scalars().one()
    await db_session.delete(restaurant)
    await db_session.commit()


@pytest.mark.asyncio
async def test_restaurant_create_invalid_duplicated(
    client_restaurant, db_session, restaurant
):
    response = await client_restaurant.post(
        "/api/v1/restaurants",
        json={"name": restaurant.name, "location": restaurant.location},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_restaurant_create_invalid_employee(client_employee, db_session):
    response = await client_employee.post(
        "/api/v1/restaurants", json={"name": "random", "location": "AUH"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_menu_create(client_restaurant, db_session, restaurant):
    response = await client_restaurant.post(
        f"/api/v1/restaurants/{restaurant.id}/menus",
        json={
            "name": uuid.uuid4().hex,
            "date_served": datetime.datetime.utcnow().isoformat(),
        },
    )

    assert response.status_code == 201
    payload = response.json()

    result = await db_session.execute(
        select(Menu).where(Menu.id == payload["id"])
    )
    menu = result.scalars().one()
    await db_session.delete(menu)
    await db_session.commit()


@pytest.mark.asyncio
async def test_menu_today(client_restaurant, db_session, menus):
    response = await client_restaurant.get("/api/v1/restaurants/menu-today")

    assert response.status_code == 200
    payload = response.json()

    assert payload.keys() == {"items", "total"}
    record = payload["items"][0]
    assert record.keys() == {
        "id",
        "name",
        "restaurant_name",
        "date_served",
        "date_added",
        "date_updated",
    }

    assert len({menu.date_served.date() for menu in menus}) > 1

    actual_date = {item["date_served"] for item in payload["items"]}
    expected_date = {datetime.datetime.now().strftime("%Y-%m-%d")}
    assert expected_date == actual_date
