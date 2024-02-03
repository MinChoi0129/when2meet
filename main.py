from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class Student(BaseModel):
    name: str = "홍길동"
    age: int = 0


app = FastAPI()

# static, templates 폴더 연결
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/student")
def get_student(student_id: Union[int, None] = -1):
    """
    이 함수는 단순한 예시로 텍스트 파일을 읽고 쓰는 함수이지만
    좀 더 발전시킨다면 데이터베이스에서 데이터(문장)을 읽어와서
    return 하게끔 코드를 수정하면 됩니다.
    """

    txt = open("students.txt", mode='r', encoding="UTF-8")
    # 모든 문장을 다 읽어서 리스트에 담기
    all_students = txt.read().splitlines()
    txt.close()

    last_sentences_number = len(all_students) - 1  # 마지막 숫자 = 길이 - 1

    if student_id == -1:
        return {"data": all_students}
    elif student_id < -1 or student_id > last_sentences_number:
        return {"data": "숫자가 너무 작거나 큽니다."}
    else:
        return {"data": [all_students[student_id]]}


@app.post("/student")
def add_student(new_student: Student):
    try:
        name = new_student.name
        age = new_student.age
        new_data = name + " " + str(age) + "\n"

        txt = open("students.txt", mode="a", encoding="UTF-8")
        txt.write(new_data)
        txt.close()
        return {"message": f"New User Created: {name}"}
    except:
        return {"success": False}

# ===================================================================================== #


@app.get("/", response_class=HTMLResponse)
def main(request: Request):  # HTML을 return
    return templates.TemplateResponse(request=request, name="main.html")
