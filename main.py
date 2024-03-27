from typing import Union
from fastapi import FastAPI, HTTPException, Depends, Request,Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Group, User
from database import SessionLocal, engine
from domain.group import group_router
from domain.user import user_router
from starlette.middleware.cors import CORSMiddleware
from database import get_db
from domain.user import user_schema,user_crud,user_router
from domain.user.user_router import user_to_dict
from sqlalchemy.orm import Session, joinedload


w2m = FastAPI()
# w2m = FastAPI(docs_url="/documentation", redoc_url=None)

# static, templates 폴더 연결
w2m.mount("/static", StaticFiles(directory="static"), name="static")
w2m.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")


# ------------ Model ------------#

w2m.include_router(group_router.router)
w2m.include_router(user_router.router)


# ------------ Url ------------#
@w2m.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@w2m.get("/signup",response_class=HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")


# ------- 갈 곳 잃은 db저장 함수 ------ #
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
        
@w2m.post("/signup/")
async def create_item(request: Request, db: Session = Depends(get_db),
                      id: str = Form(...), 
                      pw: str = Form(...), 
                      birthDay: str = Form(...), 
                      email: str = Form(...), 
                      pw2: str = Form(...), 
                      img: str = Form(...)):
    new_user = User(id=id, pw=pw, birthDay=birthDay, email=email)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return templates.TemplateResponse(request=request, name="index.html")

from fastapi.responses import RedirectResponse, Response
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from domain.user.user_crud import pwd_context
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "8df5370506fea1374a44ec6d1fbc476a0cd8c83f5d31434d3722baadf4db75ab"
ALGORITHM = "HS256"

from datetime import datetime, timezone

@w2m.post("/", response_model=user_schema.Token)
async def login_for_access_token(response:Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 사용자와 비밀번호 확인
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 사용자 이름 또는 비밀번호",
            headers={"WWW-Authenticate": "Bearer"},
        )
    exp = datetime.utcnow().astimezone(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 액세스 토큰 생성
    data = {
        "sub": user.id,
        "exp": exp
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    # 쿠키에 저장
    response.set_cookie(key="acess_token",value=access_token,expires=exp,httponly=True)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": data["sub"]
    }
from fastapi import status
   
@w2m.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response
