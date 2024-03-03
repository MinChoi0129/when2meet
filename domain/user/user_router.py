from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import User
from typing import List
from database import get_db
from domain.user import user_schema

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


@router.get("/", response_model=List[user_schema.User])
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


@router.get("/{id}", response_model=user_schema.User)
def get_user_by_code(id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).options(
        joinedload(User.groups)).first()
    user_dict = user_to_dict(user)
    return user_dict
