from pydantic import BaseModel
from typing import List
class Info_user(BaseModel):
    username: str
    password: str
    user_id: str
    
class UserCreate(BaseModel):
    users: List[Info_user]