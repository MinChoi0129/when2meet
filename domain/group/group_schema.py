from pydantic import BaseModel
from typing import List


class Group(BaseModel):
    name: str
    invitationCode: str
    pw: str
    users: List[dict]
