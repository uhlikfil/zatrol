"""enum types

Revision ID: 5042df418ca2
Revises: 
Create Date: 2022-08-30 14:37:45.686566

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "5042df418ca2"
down_revision = None
branch_labels = None
depends_on = None


type_map = {
    "EUNE": "eun1",
    "EUW": "euw1",
    "TR": "tr1",
    "RU": "ru",
    "NA": "na1",
    "BR": "br1",
    "LAN": "la1",
    "LAS": "la2",
    "OCE": "oc1",
    "KR": "kr",
    "JP": "jp1",
}


def upgrade() -> None:
    for old, new in type_map.items():
        op.execute(f"ALTER TYPE region RENAME VALUE '{old}' TO '{new}'")


def downgrade() -> None:
    for old, new in type_map.items():
        op.execute(f"ALTER TYPE region RENAME VALUE '{new}' TO '{old}'")
