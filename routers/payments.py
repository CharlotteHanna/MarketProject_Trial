
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from db import db_payments, db_products
from db.database import get_db
from db.models import DbUser
from schemas import PaymentsDisplay, PaymentsBase, UserBase
from sqlalchemy.orm import Session
from auth.oauth2 import check_admin, get_current_user


router = APIRouter(
    prefix='/payments',
    tags=['payments']
)




#Use Create Payment functionality from db_payments file
@router.post('/', response_model=PaymentsDisplay,  status_code=status.HTTP_201_CREATED)
def create_payment(request: PaymentsBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if db_products.get_seller_id(db, request.paid_product_id) is current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Owner of a product cant pay for a product he owns')

    return db_payments.create_payment(db, request, current_user.user_id)

#Use read Payment functionality from db_payments file

    #return all payments
@router.get('/', response_model=List[PaymentsDisplay])
def get_all_payments(db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    return db_payments.get_all_payments(db, current_user.user_id)

    #return payments with conditions
@router.get('/{id}', response_model=PaymentsDisplay)
def get_payment(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if current_user.is_admin:
        return db_payments.get_all_payments_admin(db)
    return db_payments.get_payment(db, id, current_user.user_id)
 
#Use Update Payment functionality from db_payments file
@router.put('/{id}', response_model=PaymentsDisplay)
def update_payment(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(check_admin)):
    return db_payments.update_payment_status(db, id)

#Use Delete Payment functionality from db_payments file
@router.delete('/{id}',  status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    return db_payments.delete_payment(db, id, current_user.user_id)
