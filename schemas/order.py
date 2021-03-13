from typing import Dict, List
from pydantic import BaseModel


class OrderItemFruitSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class OrderItemSchema(BaseModel):
    quantity: int
    price: float
    fruit: OrderItemFruitSchema

    class Config:
        orm_mode = True


class OrderCreateSchema(BaseModel):
    fruits: Dict[str, int]


class OrderUpdateSchema(BaseModel):
    fruits: Dict[str, int]


class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    order_items: List[OrderItemSchema]
    create_time: int

    class Config:
        orm_mode = True
