'''
Schemas for defining base/input models
'''
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import IntEnum

# User
#################################################

class UserPrivilege(IntEnum):
    ADMIN=0
    READ_WRITE=1
    READ_ONLY=2

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    privilige: int = Field(ge=0, le=2) # TODO add number guard 0<=x<=2
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class UserInput(SQLModel):
    username: str
    email: str
    privilige: int
    hashed_password: str
#################################################

# Item
#################################################
class Item(SQLModel, table=True):
    __tablename__ = "items"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    price: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class ItemInput(SQLModel):
    name: str = Field(index=True)
    price: float
    is_active: bool
#################################################