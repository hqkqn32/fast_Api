from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    
    class config:
        orm_mode=True


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True


class Post(PostBase):
    id:int
    created_At:datetime
    owner_id:int
    owner:UserOut


class PostCreate(PostBase):
    pass




class PostResponse(BaseModel):
    title: str
    id: int
    content: str
    published: Optional[bool]
    created_at: datetime
    owner_id: int
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id: Optional[int] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):  # token yerine büyük harf kullanımı
    access_token: str  # 'acces_token' yerine doğru yazımı
    token_type: str

class CreatedResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)

