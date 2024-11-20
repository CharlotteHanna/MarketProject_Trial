from typing import Optional
from db.models import DbCategory, DbProduct
from sqlalchemy.orm import Session
from schemas import ProductBase
from enums import ProductStatus
from sqlalchemy import or_
from sqlalchemy.orm.query import Query
from db import db_categories
from exceptions import CategoryNotFound, ProductNotFound





#Functionality in Database

#Create product in DB
def create_product(db: Session, request: ProductBase, user_id: int):
    
    category = db_categories.get_category(db, request.product_category_id)
    if not category:
                raise CategoryNotFound()
    new_product = DbProduct(
            product_name=request.product_name,
            description=request.description,
            price=request.price,
            seller_id=request.seller_id,
            image_url=request.image_url,
            product_category_id=request.product_category_id,
            product_status= ProductStatus.AVAILABLE
    )
        
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


#Return all products which not sold from DB
def get_all_products(db:Session, category_id: Optional[int], nameQuery: Optional[str], descriptionQuery: Optional[str]):
    productQuery = db.query(DbProduct).filter(DbProduct.product_status != ProductStatus.SOLD)
    
    
    if category_id:
        productQuery = productQuery.filter(DbProduct.product_category_id == category_id)

    if nameQuery:
        productQuery = productQuery.filter(DbProduct.product_name.contains(nameQuery))

    if descriptionQuery:
        productQuery = productQuery.filter(DbProduct.description.contains(descriptionQuery))

    return productQuery.all()
    




        

 #Return  Product from DB with specifiec ID         
def get_product(db: Session, id: int):
   product = db.query(DbProduct).filter(DbProduct.product_id == id).first()
   if not product:
            raise ProductNotFound()
   return product
 
# return seller_id of a product
def get_seller_id(db: Session, id: int):
     return db.query(DbProduct).filter(DbProduct.product_id == id).first().seller_id
      
#Update attributes in products table   
def update_product(db: Session, id: int, user_id: int, request: ProductBase):
   
    product = db.query(DbProduct).filter(DbProduct.product_id == id)
    product.update({
            DbProduct.product_name: request.product_name,
            DbProduct.description: request.description,
            DbProduct.price: request.price,
            DbProduct.image_url: request.image_url,
            DbProduct.product_category_id: request.product_category_id
        })
    db.commit()
    return product.first()
    
    
def update_product_status_buyer(db: Session, id: int, user_id: int ):
      db.query(DbProduct).filter(DbProduct.product_id == id).update({
            DbProduct.product_status: ProductStatus.RESERVED,
            DbProduct.buyer_id: user_id
        })
      db.commit()
      return

#Delete Product from DB    
def delete_product(db: Session, id: int):
    product = db.query(DbProduct).filter(DbProduct.product_id == id).first()
    db.delete(product)
    db.commit()
    return  






