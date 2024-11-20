from sqlalchemy.orm import Session
from db.hash import Hash
from exceptions import UserNotFound
from schemas import UserBase, UserUpdate
from db.models import DbUser
from sqlalchemy import or_
from db import db_users
from exceptions import InsufficientPermission, UserAlreadyExists, UserNotFound


#Functionality in Database

# Check if user already exists by username
def user_exists(db: Session, username: str, email: str):
    user = db.query(DbUser).filter(
    or_(DbUser.username == username, DbUser.email == email)).first()
    return user





#Create user in DB
def create_user(db: Session, request: UserBase):
        
        new_user = DbUser(
            username=request.username,
            email=request.email,
            password=Hash.bcrypt(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


#Return all users from DB   
def get_all_users(db: Session):
    return db.query(DbUser).all()
    
#Return user from DB with specific ID 
def get_user(db: Session, user_id: int):
    user =  db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not user:
                raise UserNotFound()
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise UserNotFound()
    return user

#Update attributes in users table
def update_user(db: Session, id: int, request: UserUpdate):
    
    user = db.query(DbUser).filter(DbUser.user_id == id).update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password),
        DbUser.is_admin: request.is_admin
        })
    db.commit()
    return user.first()


#Delete user from DB  
def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.user_id == id).first()
    db.delete(user)
    db.commit()
    return