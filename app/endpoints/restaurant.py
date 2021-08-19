import uuid
from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import (
    func,
    join,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.dependencies import (
    get_build_version,
    get_current_user_employee,
    get_current_user_restaurant,
    get_session,
)
from app.models.restaurant import (
    Menu,
    Restaurant,
)
from app.schemas.restaurant import (
    MenuCreateSchema,
    MenuListResponseSchema,
    MenuResponseSchema,
    RestaurantCreateSchema,
    RestaurantListResponseSchema,
    RestaurantResponseSchema,
)

router = APIRouter()

default_tag = "Restaurant"


@router.post(
    "/v1/restaurants",
    tags=[default_tag],
    dependencies=[
        Depends(get_current_user_restaurant),
        Depends(get_build_version),
    ],
    status_code=status.HTTP_201_CREATED,
    response_model=RestaurantResponseSchema,
)
async def restaurant_create(
    data: RestaurantCreateSchema, session: AsyncSession = Depends(get_session)
):
    try:
        restaurant = Restaurant(
            **data.dict(exclude_unset=True, exclude_none=True)
        )
        session.add(restaurant)
        await session.commit()
        return restaurant

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Restaurant already exists",
        )


@router.get(
    "/v1/restaurants",
    tags=[default_tag],
    dependencies=[
        Depends(get_current_user_restaurant),
        Depends(get_build_version),
    ],
    status_code=status.HTTP_200_OK,
    response_model=RestaurantListResponseSchema,
)
async def restaurant_retrieve(
    limit: int = settings.DEFAULT_PAGE_SIZE,
    offset: int = 0,
    name: str = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Restaurant)

    if name:
        query.where(Restaurant.name.ilike(f"%{name}%"))  # noqa

    query = (
        query.order_by(Restaurant.date_added.desc()).limit(limit).offset(offset)
    )
    result = await session.execute(query)
    restaurants = result.scalars().all()

    return {"items": restaurants, "total": len(restaurants)}


@router.post(
    "/v1/restaurants/{restaurant_id}/menus",
    tags=[default_tag],
    dependencies=[
        Depends(get_current_user_restaurant),
        Depends(get_build_version),
    ],
    status_code=status.HTTP_201_CREATED,
    response_model=MenuResponseSchema,
)
async def menu_create(
    data: MenuCreateSchema,
    restaurant_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        # This can be optimized by using CTE and
        # returning then join with restaurant
        menu = Menu(
            **data.dict(exclude_unset=True, exclude_none=True),
            restaurant_id=str(restaurant_id),
        )
        session.add(menu)
        await session.commit()

        query = (
            select(
                [
                    *Menu.__table__.columns,
                    Restaurant.name.label("restaurant_name"),  # noqa
                ]
            )
            .select_from(
                join(Menu, Restaurant, Restaurant.id == Menu.restaurant_id)
            )
            .where(Menu.id == menu.id)
        )

        result = await session.execute(query)
        menu = result.first()

        return menu

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Menu already exists",
        )


@router.get(
    "/v1/restaurants/menu-today",
    tags=[default_tag],
    dependencies=[
        Depends(get_current_user_employee),
        Depends(get_build_version),
    ],
    status_code=status.HTTP_200_OK,
    response_model=MenuListResponseSchema,
)
async def menu_retrieve_today(session: AsyncSession = Depends(get_session)):
    """Retrieves Today's Menu"""
    query = (
        select(
            [
                *Menu.__table__.columns,
                Restaurant.name.label("restaurant_name"),  # noqa
            ]
        )
        .select_from(
            join(Menu, Restaurant, Restaurant.id == Menu.restaurant_id)
        )
        .where(func.date(Menu.date_served) == date.today())
        .order_by(Restaurant.name)
    )

    result = await session.execute(query)
    menus = result.all()

    return {"items": menus, "total": len(menus)}
