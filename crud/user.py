from sqlalchemy.orm.session import Session
from crud.base import CRUDBase
from models.user import User
from schemas.user import UserRegisterSchema


class CRUDUser(CRUDBase[User, UserRegisterSchema, UserRegisterSchema]):
    def find_user_by_email(self, db: Session, email: str):
        return db.query(self.model).filter_by(email=email).first()


UserService = CRUDUser(User)
