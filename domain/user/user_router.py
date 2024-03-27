from fastapi import APIRouter, Depends,HTTPException
from fastapi.responses import Response

from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import User
from typing import List
from database import get_db
from domain.user import user_schema,user_crud
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt



router = APIRouter(
    prefix="/user",
)


def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "pw": user.pw,
        "email": user.email,
        "birthDay": user.birthDay,
        "groups": [group_to_dict(group) for group in user.groups],
    }


def group_to_dict(group):
    return {
        "invitationCode": group.invitationCode,
    }

# userList restAPI #


@router.get("/list", response_model=List[user_schema.UserBase])
def get_user_list(db: Session = Depends(get_db)):
    user_list = (
        db.query(User)
        .order_by(User.id)
        .options(joinedload(User.groups))
        .all()
        
    )
    user_dicts = [user_to_dict(user) for user in user_list]
    return user_dicts

# user객체 restAPI #
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

