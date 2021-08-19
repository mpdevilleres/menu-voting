from fastapi import (
    Depends,
    Header,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import (
    db,
    settings,
)
from app.models.user import (
    User,
    UserType,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


async def get_session() -> AsyncSession:
    async with db.async_session() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await session.execute(
        select(User).where(User.username == username)
    )
    user: User = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user


async def get_current_user_employee(user: User = Depends(get_current_user)):
    if user.user_type != UserType.EMPLOYEE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only employee can access this",
        )
    return user


async def get_current_user_restaurant(user: User = Depends(get_current_user)):
    if user.user_type != UserType.RESTAURANT:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only restaurant can access this",
        )
    return user


# it is assumed the build version is between 0.0 to 3.0 exclusive
async def get_build_version(
    x_build_version: float = Header(..., gt=0.0, lt=3.0)
):
    return x_build_version
