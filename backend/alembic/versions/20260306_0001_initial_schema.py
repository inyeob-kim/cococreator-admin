"""initial schema

Revision ID: 20260306_0001
Revises: 
Create Date: 2026-03-06 00:00:00
"""

from pathlib import Path

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260306_0001"
down_revision = None
branch_labels = None
depends_on = None


def _execute_sql_file() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    schema_file = backend_root / "scripts" / "cococreator_admin_mvp_schema.sql"
    sql = schema_file.read_text(encoding="utf-8")

    # Execute statements one-by-one for drivers that do not support multi-statements.
    statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
    for statement in statements:
        op.execute(sa.text(statement))


def upgrade() -> None:
    _execute_sql_file()


def downgrade() -> None:
    tables = [
        "notes",
        "payouts",
        "creator_deals",
        "orders",
        "product_listings",
        "sales_channels",
        "product_pipeline_logs",
        "products",
        "factory_capabilities",
        "factories",
        "template_flavors",
        "product_templates",
        "brands",
        "creator_contacts",
        "creators",
        "user_sessions",
        "users",
    ]
    for table in tables:
        op.execute(sa.text(f"DROP TABLE IF EXISTS {table} CASCADE"))
