import fast_api
from fastapi import FastAPI, HTTPException, status, Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
import models   # . yerine direkt import
import utils
from database import  get_db
from schemas import UserCreate,CreatedResponse
router=APIRouter(prefix="/users",tags=["users"])

@router.post("",status_code=status.HTTP_201_CREATED,response_model=CreatedResponse)
def create_user(users:UserCreate ,db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == users.email).first()
    if existing_user:
        raise HTTPException(
            status_code=404,  # HTTP 404: Not Found
            detail="Email already exists"
        )
    
    # hash password -user 
    hashed_password=utils.hash(users.password)
    users.password=hashed_password
    new_user = models.User(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    