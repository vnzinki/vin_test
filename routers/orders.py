import time
from typing import List

from auth.auth_bearer import JWTBearer
from crud.fruit import FruitService
from crud.order import OrderService
from routers.deps import get_db
from schemas.order import (OrderCreateSchema, OrderResponseSchema,
                           OrderUpdateSchema)
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm.session import Session

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[OrderResponseSchema])
async def order_get_list(db: Session = Depends(get_db), user_info=Depends(JWTBearer()), skip: int = 0, limit: int = 100):
    user_id = user_info.uid
    orders = OrderService.get_order_by_user_id(
        db, user_id=user_id, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", dependencies=[Depends(JWTBearer())], response_model=OrderResponseSchema)
async def order_get(db: Session = Depends(get_db), order_id: int = Path(..., title="order ID")):
    order = OrderService.get(db, model_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )
    return order


@router.post("/", dependencies=[Depends(JWTBearer())])
async def order_post(*, db: Session = Depends(get_db), data: OrderCreateSchema):
    order_data = {
        "user_id": 1,
        "create_time": time.time()
    }
    order = OrderService.create(db, obj_in=order_data)

    fruit_items = data.__dict__.pop('fruits')
    total_price = 0
    for fruit_key in fruit_items:
        quantity = fruit_items[fruit_key]
        fruit_item = FruitService.get(db, model_id=fruit_key)
        if fruit_item:
            order = OrderService.add_fruit(
                db, order=order, item=fruit_item, quantity=quantity)
            total_price += fruit_item.price * quantity

    order = OrderService.set_total_price(
        db, order=order, total_price=total_price)
    return order


@router.patch("/{order_id}")
async def order_patch(*, db: Session = Depends(get_db), user_info=Depends(JWTBearer()), order_id: int = Path(..., title="Order ID"), data: OrderUpdateSchema):
    order = OrderService.get(db, model_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    if user_info.uid != order.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your order",
        )

    fruit = OrderService.update(db, db_obj=order, obj_in=data)
    return fruit
