import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    class Config:
        alias_generator = lambda string: ''.join(
            word.capitalize() if i > 0 else word.lower()
            for i, word in enumerate(string.split('_'))
        )
        populate_by_alias = True
        validate_by_name = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        extra = 'forbid'


class UserResponse(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    date_joined: datetime
    
    model_config = {
        'from_attributes': True,
        'arbitrary_types_allowed': True
    }