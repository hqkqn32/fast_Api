from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import database, models
from sqlalchemy.orm import Session
from config import settings

# OAuth2 Ayarları
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCES_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Token Oluşturma
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "user_id": str(data.get("user_id"))})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Token Doğrulama
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

# Geçerli Kullanıcıyı Alma
def get_current_user(
    token: str = Depends(oauth2_schema), 
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == int(token_data.id)).first()
    if user is None:
        raise credentials_exception
    return user
