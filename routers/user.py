from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from models import Users
from database import SessionLocal
from starlette import status
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix="/user",
    tags=["User requests"],
)


class ChangePasswordRequest(BaseModel):
    new_password: str = Field(min_length=8, max_length=128)


class ChangePhoneRequest(BaseModel):
    phone_number: str = Field(min_length=11)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/get-user", status_code=status.HTTP_200_OK)
async def get_current_logged_user_data(user: user_dependency, db: db_dependency):
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, change_password_request: ChangePasswordRequest, db: db_dependency):
    hashed_new_password = bcrypt_context.hash(change_password_request.new_password)
    db_user = db.query(Users).filter(Users.id == user.get('id')).first()
    db_user.hashed_password = hashed_new_password
    db.commit()


@router.put("/change-phone", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone(user: user_dependency, change_phone_request: ChangePhoneRequest, db: db_dependency):
    db_user = db.query(Users).filter(Users.id == user.get('id')).first()
    db_user.phone_number = change_phone_request.phone_number
    db.add(db_user)
    db.commit()
