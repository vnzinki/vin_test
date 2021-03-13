
from sqlalchemy.orm.session import Session
from crud.base import CRUDBase, ModelType
from models.fruit import Fruit
from schemas.fruit import FruitCreateSchema, FruitUpdateSchema


class CRUDFruit(CRUDBase[Fruit, FruitCreateSchema, FruitUpdateSchema]):
    def change_quantity(self, db: Session, *, db_obj: ModelType, quantity: int):
        db_obj.quantity += quantity
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    pass


FruitService = CRUDFruit(Fruit)
