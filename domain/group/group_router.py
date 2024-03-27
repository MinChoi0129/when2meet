from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Group, User
from typing import List
from database import get_db
from domain.group import group_schema

router = APIRouter(
    prefix="/group",
)


def user_to_dict(user):
    return {
        "id": user.id,
    }


def group_to_dict(group: Group, include_users: bool = False) -> dict:
    result = {
        "name": group.name,
        "invitationCode": group.invitationCode,
        "pw": group.pw,
        "users": [user_to_dict(user) for user in group.users],

    }
    return result

# groupList restAPI #


@router.get("/", response_model=list[group_schema.Group])
def get_group_list(db: Session = Depends(get_db)):
    groupList = db.query(Group).order_by(Group.name).all()
    return [group_to_dict(group) for group in groupList]

# group객체 restAPI #


@router.get("/{invitation_code}", response_model=group_schema.Group)
def get_group_by_code(invitation_code: str, db: Session = Depends(get_db)):
    group = (
        db.query(Group)
        .filter(Group.invitationCode == invitation_code)
        .options(joinedload(Group.users))
        .first()
    )
    return group_to_dict(group)
