from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from db.models import DbUser
from schemas import UserBase, UserDisplay, UserUpdate
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_users
from auth.oauth2 import check_admin, get_current_user
from exceptions import InsufficientPermission, UserAlreadyExists, UserNotFound

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#Use Create User functionality from db_users file
@router.post('/', response_model=UserDisplay,  status_code=status.HTTP_201_CREATED)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    user = db_users.user_exists(db, request.username, request.email)
    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User with this username or email already exists')

    return db_users.create_user(db, request)







#Use read User functionality from db_users file

#return all users
@router.get('/', response_model=List[UserDisplay],  status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db), current_user: DbUser = Depends(check_admin)):
        return db_users.get_all_users(db)


#return User with conditions
@router.get('/{id}', response_model=UserDisplay,  status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
# check if it is the same user or admin
        if not (current_user.user_id is id or current_user.is_admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions to perform this action')

        return db_users.get_user(db, id)





#Use Update User functionality from db_users file
@router.put('/{id}', response_model=UserDisplay,  status_code=status.HTTP_200_OK)
def update_user(id: int, request: UserUpdate, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
        # check if it is the same user or admin
        if not (current_user.user_id is id or current_user.is_admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have enough permissions to perform this action")

        # make a normal user an admin
        if request.is_admin and not current_user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to make a user admin.")

        # if someone tries to change the role of an admin
        user = db.query(DbUser).filter(DbUser.user_id == id).first()
        if not request.is_admin and user.is_admin:
            if not current_user.is_admin:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to revoke admin rights.")
        db_users.get_user(db, id)
        return db_users.update_user(db, id, request)


#Use Delete User functionality from db_users file
@router.delete('/{id}',  status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
        
# check if it is the same user or admin
        if not (current_user.user_id is id or current_user.is_admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have enough permissions to perform this action")

        first_admin = db.query(DbUser).filter(DbUser.is_admin==True).first()
        #admin can not be deleted
        if id == first_admin.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin can not be deleted")
        
        db_users.get_user(db, id)
        return db_users.delete_user(db, id)