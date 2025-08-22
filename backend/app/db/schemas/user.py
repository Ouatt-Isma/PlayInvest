from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    birthdate: Optional[date]
    avatar_url: Optional[str]
    username: Optional[str]
    profession: Optional[str]
    living_country: Optional[str]
    origin_country: Optional[str]
    age: Optional[str]
    currency: Optional[str]
    # email: str