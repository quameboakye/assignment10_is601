import os


def _normalize_url(url: str) -> str:
    """Force the psycopg 3 driver so every SQLAlchemy version agrees."""
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


class Settings:
    DATABASE_URL: str = _normalize_url(
        os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")
    )


settings = Settings()
