import datetime

from asyncpg import exceptions
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.dependencies import (
    get_build_version,
    get_current_user_employee,
    get_session,
)
from app.models.user import User
from app.models.vote import Vote
from app.schemas.vote import (
    VoteSchema,
    VoteV1CreateSchema,
    VoteV1ResponseSchema,
    VoteV2CreateSchema,
    VoteV2ResponseSchema,
)

router = APIRouter()

default_tag = "Vote"


def is_voting_open(utcnow: datetime.datetime):
    # check if vote entered is within the allowed time
    start = datetime.datetime.utcnow().replace(
        hour=settings.VOTING_TIME_START_UTC.hour,
        minute=settings.VOTING_TIME_START_UTC.minute,
        second=0,
        microsecond=0,
    )
    end = start + datetime.timedelta(
        seconds=settings.VOTING_TIME_LENGTH_SECONDS
    )
    return start <= utcnow <= end


async def create_votes(
    data: list[VoteSchema], user: User, session: AsyncSession
):
    utcnow = datetime.datetime.utcnow()

    if not is_voting_open(utcnow):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Voting is close",
        )
    votes = []
    for d in data:
        vote = Vote(**d.dict(), user_id=user.id, date_voted=utcnow.date())
        votes.append(vote)
        session.add(vote)

    try:
        await session.commit()

    except IntegrityError as e:
        # the reason we use sqlstate here is that sqlalchemy
        # doesn't raise the driver's exception as native
        await session.rollback()
        if e.orig.sqlstate == exceptions.ForeignKeyViolationError.sqlstate:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Menu ID does not exist",
            )
        elif e.orig.sqlstate == exceptions.UniqueViolationError.sqlstate:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Vote already registered",
            )

        raise e

    return votes


@router.post(
    "/v2/votes",
    tags=[default_tag],
    dependencies=[
        Depends(get_current_user_employee),
        Depends(get_build_version),
    ],
    status_code=status.HTTP_201_CREATED,
    response_model=VoteV2ResponseSchema,
)
async def vote_create_v2(
    data: VoteV2CreateSchema,
    user: User = Depends(get_current_user_employee),
    session: AsyncSession = Depends(get_session),
):
    votes = await create_votes(data.votes, user, session)
    return {"votes": votes}


@router.post(
    "/v1/votes",
    deprecated=True,
    tags=[default_tag],
    dependencies=[Depends(get_build_version)],
    status_code=status.HTTP_201_CREATED,
    response_model=VoteV1ResponseSchema,
)
async def vote_create_v1(
    data: VoteV1CreateSchema,
    user: User = Depends(get_current_user_employee),
    session: AsyncSession = Depends(get_session),
):
    # since this is a single vote it is assumed that points is always max
    values = [VoteSchema(menu_id=data.menu_id, point=3)]
    vote, *_ = await create_votes(values, user, session)

    return vote
