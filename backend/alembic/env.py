from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.core.config import settings  # noqa: E402
from app.models.base import Base  # noqa: E402

# Import models so metadata is complete.
from app.modules.auth import model as auth_model  # noqa: F401,E402
from app.modules.brands import model as brands_model  # noqa: F401,E402
from app.modules.creators import model as creators_model  # noqa: F401,E402
from app.modules.factories import model as factories_model  # noqa: F401,E402
from app.modules.finance import model as finance_model  # noqa: F401,E402
from app.modules.orders import model as orders_model  # noqa: F401,E402
from app.modules.product_pipeline import model as product_pipeline_model  # noqa: F401,E402
from app.modules.products import model as products_model  # noqa: F401,E402
from app.modules.templates import model as templates_model  # noqa: F401,E402

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
