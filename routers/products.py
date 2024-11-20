from typing import List, Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from db.models import DbUser
from exceptions import CategoryNotFound, InsufficientPermission
from schemas import ProductBase, ProductDisplay
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
       
        return db_products.create_product(db, request, current_user.user_id)
    

#Use read Product functionality from db_products file
        #return all products which not sold
@router.get('/', response_model=List[ProductDisplay],  status_code=status.HTTP_200_OK)
def get_all_products(category_id: Optional[int] = None, nameQuery: Optional[str] = None, descriptionQuery: Optional[str] = None,db: DbUser = Depends(get_db)):
        return db_products.get_all_products(db, category_id, nameQuery, descriptionQuery)
        


        #return products with conditions
@router.get('/{id}', response_model=ProductDisplay,  status_code=status.HTTP_200_OK)
def get_product(id: int, db: Session = Depends(get_db) ):
       return db_products.get_product(db, id)
        
       
   
     

#Use Update Product functionality from db_products file
@router.put('/{id}', response_model=ProductDisplay,  status_code=status.HTTP_200_OK)
def update_product(id: int, request: ProductBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
        db_products.get_product(db, id)
        if db_products.get_seller_id(db, id) != current_user.user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have enough permissions to perform this action')
     
        return db_products.update_product(db, id, request)
  
                
       
       
    
  

#Use Delete Product functionality from db_products file
@router.delete('/{id}',  status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
        db_products.get_product(db, id)
        
        if db_products.get_seller_id(db, id) != current_user.user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have enough permissions to perform this action')
     
        return db_products.delete_product(db, id)





   