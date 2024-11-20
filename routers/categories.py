
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from db import db_categories
from db.database import get_db
from db.models import DbUser
from schemas import CategoryDisplay, CategoryBase, UserBase
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/categories',
    tags=['categories']
)




#Use Create Category functionality from db_categories file
@router.post('/', response_model=CategoryDisplay,  status_code=status.HTTP_201_CREATED)
def create_category(request: CategoryBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if not  current_user.is_admin:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions to perform this action')
        
    return db_categories.create_category(db, request)

#Use read Category functionality from db_categories file

    #return all categories
@router.get('/', response_model=List[CategoryDisplay])
def get_all_categories(db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    
    return db_categories.get_all_categories(db)


#Use Update Category functionality from db_categories file
@router.put('/{id}', response_model=CategoryDisplay)
def update_category(id: int,request: CategoryBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
     if not  current_user.is_admin:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions to perform this action')
     db_categories.get_category(db, id)
     return db_categories.update_category(db, id, request)

#Use Delete Category functionality from db_categories file
@router.delete('/{id}',  status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if not  current_user.is_admin:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions to perform this action')
    db_categories.get_category(db, id)
    return db_categories.delete_category(db, id)
