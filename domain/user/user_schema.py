from pydantic import BaseModel, EmailStr, Field, validator
from typing import List,Optional  

class UserBase(BaseModel):
    id: str
    pw: str
    birthDay: str
    email: str
class User(UserBase):
    groups: List[dict]
    img: Optional[str]  

class UserCreate(UserBase):
    pw2: str
    img: Optional[str]  

    @validator('id', 'pw', 'pw2', 'birthDay')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('필수 답변입니다.')
        return v

    @validator('pw2')
    def passwords_match(cls, v, values):
        if 'pw' in values and v != values['pw']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
class Token(BaseModel):
    access_token: str
    token_type: str
    username:str
