from models.fruit import Fruit
from sqlalchemy.orm.session import Session
from crud.base import CRUDBase
from models.order import Order, OrderItem
from schemas.order import OrderCreateSchema, OrderUpdateSchema


class CRUDOrder(CRUDBase[Order, OrderCreateSchema, OrderUpdateSchema]):

    def get_order_by_user_id(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter_by(user_id=user_id).offset(skip).limit(limit).all()

    def add_fruit(self, db: Session, order: Order, item: Fruit, quantity: int):
        order.order_items.append(OrderItem(item=item, quantity=quantity))
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    def set_total_price(self, db: Session, order: Order, total_price: float):
        order.total_price = total_price
        db.add(order)
        db.commit()
        db.refresh(order)
        return order


OrderService = CRUDOrder(Order)
