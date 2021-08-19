"""'init'

Revision ID: ff25a230dd76
Revises: 
Create Date: 2021-08-17 22:47:57.641898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ff25a230dd76"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "restaurant",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("date_added", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("location", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="backend",
    )
    op.create_table(
        "user",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("date_added", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("username", sa.Text(), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column(
            "user_type",
            postgresql.ENUM("EMPLOYEE", "RESTAURANT", name="usertype"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="backend",
    )
    op.create_table(
        "menu",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("date_added", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("date_served", sa.Date(), nullable=True),
        sa.Column("restaurant_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["restaurant_id"],
            ["backend.restaurant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="backend",
    )
    op.create_table(
        "vote",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("date_added", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("menu_id", postgresql.UUID(), nullable=True),
        sa.Column("user_id", postgresql.UUID(), nullable=True),
        sa.Column("point", sa.Integer(), nullable=False),
        sa.Column("date_voted", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["backend.menu.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["backend.user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("menu_id", "user_id", "date_voted", name="uq_vote"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vote")
    op.drop_table("menu", schema="backend")
    op.drop_table("user", schema="backend")
    op.drop_table("restaurant", schema="backend")
    # ### end Alembic commands ###