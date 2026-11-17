import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DEFAULT_DATABASE_URL = f"sqlite:///{Path(__file__).resolve().parents[3] / 'cupcakes.db'}"


def get_database_url() -> str:
    configured_url = os.environ.get("DATABASE_URL")
    if configured_url is None:
        return DEFAULT_DATABASE_URL

    configured_url = configured_url.strip()
    if not configured_url:
        raise RuntimeError("DATABASE_URL está definida, mas vazia.")
    if configured_url.startswith("postgres://"):
        configured_url = configured_url.replace("postgres://", "postgresql+psycopg://", 1)
    if configured_url.startswith("postgresql://"):
        configured_url = configured_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if configured_url.startswith("postgresql+psycopg://"):
        if "sslmode=disable" in configured_url.lower():
            raise RuntimeError("DATABASE_URL PostgreSQL deve usar SSL.")
        if "sslmode=" not in configured_url.lower():
            configured_url += "&sslmode=require" if "?" in configured_url else "?sslmode=require"
    return configured_url


DATABASE_URL = get_database_url()
IS_SQLITE = DATABASE_URL.startswith("sqlite")
engine_options = {"connect_args": {"check_same_thread": False}} if IS_SQLITE else {"pool_pre_ping": True}
engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


if IS_SQLITE:
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
