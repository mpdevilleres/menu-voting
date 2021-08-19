import factory
from app.models.restaurant import (
    Menu,
    Restaurant,
)


class RestaurantFactory(factory.Factory):
    class Meta:
        model = Restaurant

    name = factory.Faker("bothify", text="???????")
    location = factory.Faker("bothify", text="???????")


class MenuFactory(factory.Factory):
    class Meta:
        model = Menu

    name = factory.Faker("bothify", text="???????")
