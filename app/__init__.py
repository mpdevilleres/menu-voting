from importlib import metadata

from app.config import Settings

try:
    # this is the name of the application, located in pyproject.toml
    version = metadata.version('menu_voting')
except metadata.PackageNotFoundError:
    version = "unknown"

settings = Settings()
