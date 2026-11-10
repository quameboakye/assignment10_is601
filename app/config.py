import os

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/mydb"
    )

settings = Settings()
