from db.models import DbCategory
from sqlalchemy.orm import Session
from exceptions import CategoryNotFound
from schemas import CategoryBase
from fastapi import HTTPException, status



#Functionality in Database

#Create category in DB
def create_category(db: Session, request: CategoryBase):
    new_category = DbCategory(
            category_name=request.category_name,
            
    )
        
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


#Return all categories 
def get_all_categories(db:Session):
    return db.query(DbCategory).all()
    
#Return category from DB with specific ID 
def get_category(db: Session, id: int):
    category =  db.query(DbCategory).filter(DbCategory.category_id == id).first()
    if not category:
            raise CategoryNotFound()
    return category


#Update category
def update_category(db: Session, id: int, request: CategoryBase):
    category = db.query(DbCategory).filter(DbCategory.category_id == id)
    category.update({
            DbCategory.category_name: request.category_name
        })
    db.commit()
    return category.first()
    
    


#Delete Category from DB    
def delete_category(db: Session, id: int):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first()
    db.delete(category)
    db.commit()
    return 






