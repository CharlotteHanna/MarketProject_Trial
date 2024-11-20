
from typing import List
from fastapi import APIRouter, Depends
from db import db_categories
from db.database import get_db
from schemas import CategoryDisplay, CategoryBase, UserBase
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/categories',
    tags=['categories']
)




#Use Create Category functionality from db_categories file
@router.post('/', response_model=CategoryDisplay)
def create_category(request: CategoryBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_categories.create_category(db, request)

#Use read Category functionality from db_categories file

    #return all categories
@router.get('/', response_model=List[CategoryDisplay])
def get_all_categories(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_categories.get_all_categories(db)


#Use Update Category functionality from db_categories file
@router.put('/{id}')
def update_category(id: int,request: CategoryBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_categories.update_category(db, id, request)

#Use Delete Category functionality from db_categories file
@router.delete('/{id}')
def delete_category(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_categories.delete_category(db, id)
