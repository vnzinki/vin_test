
from models.fruit import Fruit
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.base import Base
import time


class OrderItem(Base):
    order_id = Column(Integer, ForeignKey("order.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("fruit.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    fruit = relationship(Fruit, lazy="joined")

    def __init__(self, item, quantity):
        self.item_id = item.id
        self.price = item.price
        self.quantity = quantity


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    note = Column(String, nullable=True)
    create_time = Column(Integer, default=time.time())
    total_price = Column(Float)
    order_items = relationship(
        OrderItem, cascade="all, delete-orphan", backref="order"
    )
