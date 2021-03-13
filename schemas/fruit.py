from typing import Optional
from pydantic import BaseModel


class FruitBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class FruitCreateSchema(FruitBaseSchema):
    pass


class FruitUpdateSchema(FruitBaseSchema):
    name: Optional[str]
    description: Optional[str] = None
    price: Optional[float]
    pass


class FruitResponseSchema(FruitBaseSchema):
    id: int

    class Config:
        orm_mode = True
