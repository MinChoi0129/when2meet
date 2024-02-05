from typing import Union
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Group, User
from database import SessionLocal, engine
from domain.group import group_router
from domain.user import user_router
from starlette.middleware.cors import CORSMiddleware


w2m = FastAPI()

# static, templates 폴더 연결
w2m.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



#------------ Model ------------#

w2m.include_router(group_router.router)
w2m.include_router(user_router.router)


#------------ Url ------------#
@w2m.get("/",response_class =HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request,name="index.html")

