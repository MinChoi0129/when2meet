from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id:str
    pw:str
    birthDay:str
    email:str
    groups:List[dict]|None=None
    