from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import  datetime, timedelta, timezone
from jose import jwt
from db.database import get_db
from sqlalchemy.orm import Session
from jose.exceptions import JWTError
from db import db_users
from db.models import DbUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  # sourcery skip: aware-datetime-for-utc, simplify-dictionary-update
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  # sourcery skip: raise-from-previous-error
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = db.query(DbUser).filter(DbUser.username == username).first() 
  if user is None:

    raise credentials_exception

  return user

# Admin checking

def check_admin(current_user: DbUser = Depends(get_current_user)):

    if not current_user.is_admin:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Only admins can access this resource.",

            headers={"WWW-Authenticate": "Bearer"},

        )

    return current_user