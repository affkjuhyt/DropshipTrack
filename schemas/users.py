import datetime
from optparse import Option
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Option[str] = None
    last_name: Option[str] = None
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: str
    first_name: Option[str] = None
    last_name: Option[str] = None
    is_active: bool
    date_joined: datetime
    
    class Config:
        from_attributes = True