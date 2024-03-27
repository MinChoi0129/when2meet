from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(id=user_create.id,
                   pw=pwd_context.hash(user_create.pw),
                   email=user_create.email,
                   birthDay=user_create.birthDay,
                   groups=[]
                   )
    db.add(db_user)
    db.commit()
    
def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.id == user_create.id) |
        (User.email == user_create.email)
    ).first()
    
def get_user(db: Session, username: str):
    return db.query(User).filter(User.id == username).first()