# from dotenv import load_dotenv

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --------------------------------------------------
# Fix Python path (CRITICAL for Docker + local)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE_DIR, "app")

# load_dotenv(os.path.join(os.path.dirname(BASE_DIR), ".env"))

sys.path.append(BASE_DIR)
sys.path.append(APP_DIR)

# --------------------------------------------------
# Alembic config
# --------------------------------------------------
config = context.config

# Ensure script_location is correct
config.set_main_option("script_location", os.path.join(BASE_DIR, "alembic"))

# Load DB URL from environment (DO NOT hardcode)
database_url = os.getenv("DATABASE_URL")
print("=" * 60)
print("DATABASE_URL:", repr(database_url))
print("=" * 60)
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --------------------------------------------------
# Import your models AFTER fixing path
# --------------------------------------------------
from app.db.base import Base  # noqa: E402

import app.models #noqa: E402

target_metadata = Base.metadata


# --------------------------------------------------
# Migration logic
# --------------------------------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    print("[1] Starting migrations")

    configuration = config.get_section(config.config_ini_section)
    print("[2] Configuration loaded")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    print("[3] Engine created")

    with connectable.connect() as connection:
        print("[4] Connected to database")
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        print("[5] Context configured")

        with context.begin_transaction():
            print("[6] Running migrations")
            context.run_migrations()

        print("[7] Done")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
