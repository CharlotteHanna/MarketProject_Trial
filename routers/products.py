from typing import List, Optional  
from fastapi import APIRouter, Depends, HTTPException, Query, status
from db.models import DbUser
from exceptions import CategoryNotFound, InsufficientPermission
from schemas import ProductBase, ProductDisplay, ProductUpdate
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_categories, db_products
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

#Use Create Product functionality from db_products file
@router.post('/', response_model=ProductDisplay,  status_code=status.HTTP_201_CREATED)
def create_product(request: ProductBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
        # if current_user.user_id is not request.seller_id:
        if not (current_user.user_id is request.seller_id or current_user.is_admin):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User should provide his own id in seller_id')
        return db_products.create_product(db, request, current_user.user_id)
    

#Use read Product functionality from db_products file
        #return all products which not sold
@router.get('/', response_model=List[ProductDisplay],  status_code=status.HTTP_200_OK)
def get_all_products(category_id: Optional[int] = Query(None, description="Filter by category ID"), nameQuery: Optional[str] = Query(None, description="Filter by product name"), descriptionQuery: Optional[str] = Query(None, description="Filter by product description"),db: DbUser = Depends(get_db)):
        return db_products.get_all_products(db, category_id, nameQuery, descriptionQuery)
        


        #return products with conditions
@router.get('/{id}', response_model=ProductDisplay,  status_code=status.HTTP_200_OK)
def get_product(id: int, db: Session = Depends(get_db) ):
       return db_products.get_product(db, id)
        
       
   
     

#Use Update Product functionality from db_products file
@router.put('/{id}', response_model=ProductDisplay,  status_code=status.HTTP_200_OK)
def update_product(id: int, request: ProductUpdate, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
        db_products.get_product(db, id)
        if not (db_products.get_seller_id(db, id) is current_user.user_id or current_user.is_admin):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions to perform this action')
     
        return db_products.update_product(db, id, request)
  
                
       


#Use Delete Product functionality from db_products file
@router.delete('/{id}',  status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
        db_products.get_product(db, id)
        
        if not (db_products.get_seller_id(db, id) is current_user.user_id or current_user.is_admin):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions to perform this action')
     
        return db_products.delete_product(db, id)





   