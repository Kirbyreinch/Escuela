from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    id: int 
    username: str
    password: str


class UserCreate(UserBase):
    rol: str

class UserUpdate(BaseModel):
    username: str
    rol: str


class UserInfoBase(BaseModel):
    name: str
    last_name: str

class UserInfoCreate(UserInfoBase):
    email: str
    tel: str
    escuela: str

class UserInfoUpdate(BaseModel):
    id: str
    name: str
    last_name: str
    email: str
    tel: str
    escuela: str