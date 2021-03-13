from auth.auth_handler import signJWT
from crud.user import UserService
from routers.deps import get_db
from schemas.user import UserLoginSchema, UserRegisterSchema
from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Body, Depends
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/user/signup")
async def create_user(db: Session = Depends(get_db), user: UserRegisterSchema = Body(...)):
    # too lazy for now
    user.password = pwd_context.hash(user.password)
    db_user = UserService.create(db, obj_in=user)
    return signJWT(db_user)


@router.post("/user/login")
async def user_login(db: Session = Depends(get_db), user: UserLoginSchema = Body(...)):
    db_user = UserService.find_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password.",
        )

    return signJWT(db_user)
