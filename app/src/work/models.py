from sqlalchemy import TIMESTAMP, Table, Column, Integer, String, MetaData, ForeignKey

from src.database import metadata


workplace = Table(
    "workplace",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(64), nullable=False),
    Column("key", String, nullable=False),
)

post = Table(
    "post",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32), nullable=False),
    Column("description", String(512)),
    Column("workplace_id", Integer, ForeignKey("workplace.id"), nullable=False),
    Column("date_create", TIMESTAMP, nullable=False),
)

