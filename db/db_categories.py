from db.models import DbCategory
from sqlalchemy.orm import Session
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
    return db.query(DbCategory).filter(DbCategory.category_id == id).first()


#Update category
def update_category(db: Session, id: int, request: CategoryBase):
    category = db.query(DbCategory).filter(DbCategory.category_id == id) 
    if not category.first(): #this is our record
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {id} was not found")

    category.update({
            DbCategory.category_name: request.category_name
         })
    db.commit()
    return {'message': f'Category with id: {id} was updated'}
    
    


#Delete Category from DB    
def delete_category(db: Session, id: int):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {id} was not found")
    
    db.delete(category)
    db.commit()
    return {'message': f'Category with id: {id} was deleted'}  # Return the deleted category object  






