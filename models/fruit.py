
from sqlalchemy import Column, Integer, Float, String
from db.base import Base


class Fruit(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
