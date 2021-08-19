from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import (
    get_build_version,
    get_session,
)
from app.models.user import User
from app.schemas.user import (
    TokenSchema,
    UserCreateSchema,
    UserResponseSchema,
)

router = APIRouter()

default_tag = "User"


@router.post(
    "/v1/users",
    tags=[default_tag],
    dependencies=[Depends(get_build_version)],
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchema,
)
async def user_create(
    data: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    if not data.name:
        data.name = data.username.title()

    user = User(**data.dict(exclude_none=True, exclude_unset=True))
    session.add(user)
    await session.commit()

    return user


@router.post(
    "/v1/login",
    tags=[default_tag],
    dependencies=[Depends(get_build_version)],
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
)
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """Login as a Restaurant or an Employee"""
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    result = await session.execute(
        select(User).where(User.username == form_data.username)
    )
    user: User = result.scalars().first()
    if user and user.verify_password(form_data.password):
        access_token = user.create_access_token()
        return {"access_token": access_token, "token_type": "bearer"}

    raise exception
