import random

import factory
from app.models.user import (
    User,
    UserType,
)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("bothify", text="???????")
    username = factory.Faker("bothify", text="???????")
    user_type = random.choice(list(UserType))
    password = factory.Faker("bothify", text="????####")
