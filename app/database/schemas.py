from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class Item(SQLModel, table=True):
    __tablename__ = "items"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    price: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None