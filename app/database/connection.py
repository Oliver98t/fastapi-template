
import os
from sqlmodel import SQLModel, create_engine, Session

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "oli98")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# SQLModel engine
engine = create_engine(DATABASE_URL, echo=True)


# Dependency to get DB session
def get_db():
    with Session(engine) as session:
        yield session