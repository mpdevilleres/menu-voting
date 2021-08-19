import asyncio
import importlib
import logging
import pkgutil
from logging.config import fileConfig

from alembic import context
from sqlalchemy import (
    engine_from_config,
    pool,
)
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql.ddl import CreateSchema

from app import (
    db,
    settings,
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app import models

target_metadata = db.BaseModel.metadata

for importer, modname, ispkg in pkgutil.iter_modules(models.__path__):
    if not ispkg:
        importlib.import_module("." + modname, models.__name__)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
config.set_main_option("sqlalchemy.url", settings.POSTGRES_DATABASE_URI)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=settings.POSTGRES_DATABASE_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        version_table_schema=settings.BACKEND_DATABASE_SCHEMA,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=settings.BACKEND_DATABASE_SCHEMA,
        compare_type=True,
    )

    with context.begin_transaction():
        if not connection.dialect.has_schema(
            connection, settings.BACKEND_DATABASE_SCHEMA
        ):
            connection.execute(CreateSchema(settings.BACKEND_DATABASE_SCHEMA))
            logging.warning(
                f"schema {settings.BACKEND_DATABASE_SCHEMA} created"
            )

        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
