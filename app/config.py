import datetime

from pydantic import BaseSettings
from pydantic.types import conint


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True

    DEBUG: bool = False

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "internal"
    BACKEND_DATABASE_SCHEMA: str = "backend"

    @property
    def POSTGRES_DATABASE_URI(self):  # noqa
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_SECRET_KEY = "w8sBCFELhruhPCVFYQ9Ms59WhaEuxS9K"
    JWT_ALGORITHM = "HS256"

    DEFAULT_PAGE_SIZE: int = 100

    VOTING_TIME_START_UTC: datetime.time = "1:00"
    VOTING_TIME_LENGTH_SECONDS: conint(gt=0) = 1 * 60 * 60  # H * M * S
