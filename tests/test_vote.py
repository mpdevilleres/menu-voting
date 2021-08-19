import datetime
import uuid

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from sqlalchemy import select

from app.endpoints.vote import (
    create_votes,
    is_voting_open,
)
from app.models.vote import Vote
from app.schemas.vote import VoteSchema


@pytest.mark.asyncio
async def test_voting_period(client_employee, db_session):
    with freeze_time("2020-02-02 01:30"):
        utcnow = datetime.datetime.utcnow()
        assert is_voting_open(utcnow)

    with freeze_time("2020-02-02 00:30"):
        utcnow = datetime.datetime.utcnow()
        assert not is_voting_open(utcnow)

    with freeze_time("2020-02-02 03:30"):
        utcnow = datetime.datetime.utcnow()
        assert not is_voting_open(utcnow)


@pytest.mark.asyncio
@freeze_time("2020-02-02 01:30")
async def test_vote_create_votes_invalid_missing_menu_id(
    client_employee, user_employee, db_session
):
    data = [VoteSchema(menu_id=uuid.uuid4(), point=3)]
    with pytest.raises(HTTPException) as exception_info:
        await create_votes(data, user_employee, db_session)

    assert "Menu ID does not exist" == exception_info.value.detail


@pytest.mark.asyncio
@freeze_time("2020-02-02 01:30")
async def test_vote_create_votes_invalid_duplicated_vote(
    client_employee, user_employee, db_session, menu
):
    data = [
        VoteSchema(menu_id=menu.id, point=3),
        VoteSchema(menu_id=menu.id, point=3),
    ]
    with pytest.raises(HTTPException) as exception_info:
        await create_votes(data, user_employee, db_session)

    assert "Vote already registered" == exception_info.value.detail


@pytest.mark.asyncio
@freeze_time("2020-02-02 01:30")
async def test_vote_create_v1_valid(client_employee, db_session, menu):
    response = await client_employee.post(
        "/api/v1/votes", json={"menu_id": str(menu.id)}
    )

    payload = response.json()
    assert response.status_code == 201
    assert payload.keys() == {"id", "menu_id", "user_id"}

    result = await db_session.execute(
        select(Vote).where(Vote.id == payload["id"])
    )
    vote = result.scalars().one()
    await db_session.delete(vote)
    await db_session.commit()


@pytest.mark.asyncio
@freeze_time("2020-02-02 01:30")
async def test_vote_create_v2_valid(client_employee, db_session, menus):
    response = await client_employee.post(
        "/api/v2/votes",
        json={
            "votes": [
                {"menu_id": menus[0].id, "point": 3},
                {"menu_id": menus[1].id, "point": 2},
                {"menu_id": menus[2].id, "point": 1},
            ]
        },
    )

    payload = response.json()
    assert response.status_code == 201
    assert payload.keys() == {"votes"}
    assert payload["votes"][0].keys() == {"id", "menu_id", "user_id", "point"}

    result = await db_session.execute(
        select([Vote]).where(Vote.id.in_([i["id"] for i in payload["votes"]]))
    )
    votes = result.scalars().all()
    for vote in votes:
        await db_session.delete(vote)
    await db_session.commit()
