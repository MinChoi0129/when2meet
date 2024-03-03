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


# ------------ Model ------------#

w2m.include_router(group_router.router)
w2m.include_router(user_router.router)


# ------------ Url ------------#
@w2m.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@w2m.get("/myGroup/{invitation_code}", response_class=HTMLResponse)
def groupPage(request: Request, invitation_code: str):
    print(invitation_code, "로 접속 중")
    return templates.TemplateResponse(request=request, name="groupPage/groupPage.html")


@w2m.get("/myGroups", response_class=HTMLResponse)
def myGroups(request: Request):
    return templates.TemplateResponse(request=request, name="myPage/myGroups.html")


@w2m.get("/myTable", response_class=HTMLResponse)
def myTable(request: Request):
    return templates.TemplateResponse(request=request, name="myPage/myTable.html")


@w2m.get("/setting", response_class=HTMLResponse)
def setting(request: Request):
    return templates.TemplateResponse(request=request, name="myPage/setting.html")
