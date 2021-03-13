from typing import List

from auth.auth_bearer import JWTBearer
from crud.fruit import FruitService
from routers.deps import get_db
from schemas.fruit import (FruitCreateSchema, FruitResponseSchema,
                           FruitUpdateSchema)
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models.user import UserRole
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/fruits",
    tags=["fruits"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[FruitResponseSchema])
async def fruit_get_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    fruits = FruitService.get_multi(db, skip=skip, limit=limit)
    return fruits


@router.post("/", dependencies=[Depends(JWTBearer(scope=UserRole.ADMIN.value))], response_model=FruitResponseSchema)
async def fruit_post(*, db: Session = Depends(get_db), data: FruitCreateSchema):
    fruit = FruitService.create(db, obj_in=data)
    return fruit


@router.patch("/{fruit_id}", dependencies=[Depends(JWTBearer(scope=UserRole.ADMIN.value))], response_model=FruitResponseSchema)
async def fruit_patch(*, db: Session = Depends(get_db), fruit_id: int = Path(..., title="Fruit ID"), data: FruitUpdateSchema):
    fruit = FruitService.get(db, model_id=fruit_id)
    if not fruit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found.",
        )

    fruit = FruitService.update(db, db_obj=fruit, obj_in=data)
    return fruit


@router.delete("/{fruit_id}", dependencies=[Depends(JWTBearer(scope=UserRole.ADMIN.value))])
async def fruit_delete(db: Session = Depends(get_db), fruit_id: int = Path(..., title="Fruit ID")):
    fruit = FruitService.get(db, model_id=fruit_id)
    if not fruit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found.",
        )
    FruitService.remove(db, model_id=fruit_id)
    return {"message": f"Fruit with ID = {fruit_id} deleted."}
