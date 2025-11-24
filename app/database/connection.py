import os
from sqlmodel import SQLModel, create_engine, Session

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLModel engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get DB session
def get_db():
    with Session(engine) as session:
        yield session
