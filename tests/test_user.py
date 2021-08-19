import pytest
from sqlalchemy import select

from app.models.user import User


@pytest.mark.asyncio
async def test_generate_hash_password(client, db_session, user_employee):
    assert "argon2" in user_employee.password


@pytest.mark.asyncio
async def test_user_create(client, db_session):
    response = await client.post(
        "/api/v1/users",
        json={"username": "user@example.com", "password": "random_password"},
    )
    assert response.status_code == 201
    payload = response.json()

    result = await db_session.execute(
        select(User).where(User.id == payload["id"])
    )
    user = result.scalars().one()
    assert user
    assert user.password != "random_password"

    await db_session.delete(user)
    await db_session.commit()


@pytest.mark.asyncio
async def test_login(client, db_session, user_employee):
    user_employee.password = "random_password"
    db_session.add(user_employee)
    await db_session.commit()

    response = await client.post(
        "/api/v1/login",
        data={
            "username": user_employee.username,
            "password": "random_password",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["access_token"]
    assert payload["token_type"] == "bearer"
