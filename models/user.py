
from enum import IntEnum
from sqlalchemy import Column, Integer, String
from db.base import Base


class UserRole(IntEnum):
    USER = 1
    ADMIN = 2


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, default=0)
    role = Column(Integer, default=UserRole.USER.value)
