import pytest

from app.database.connection import DEFAULT_DATABASE_URL, get_database_url


def test_database_defaults_to_sqlite_when_variable_is_absent(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_database_url() == DEFAULT_DATABASE_URL
    assert get_database_url().startswith("sqlite:///")


def test_database_normalizes_postgresql_urls(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://user:password@localhost:5432/app")
    assert get_database_url() == "postgresql+psycopg://user:password@localhost:5432/app?sslmode=require"

    monkeypatch.setenv("DATABASE_URL", "postgresql://user:password@localhost:5432/app?sslmode=require")
    assert get_database_url() == "postgresql+psycopg://user:password@localhost:5432/app?sslmode=require"


def test_postgresql_ssl_can_not_be_disabled(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:password@localhost:5432/app?sslmode=disable")
    with pytest.raises(RuntimeError, match="SSL"):
        get_database_url()


def test_empty_database_url_does_not_fallback_to_sqlite(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", " ")
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        get_database_url()
