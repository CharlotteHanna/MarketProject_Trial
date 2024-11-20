from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm.session import Session
from db import db_products
from db.models import DbPayment, DbProduct
from enums import ProductStatus
from exceptions import CanNotAccessPayment, CanNotDeletePayment, CanNotPayForProduct, CanNotPayForReservedProduct, PaymentNotFound
from schemas import PaymentsBase
from enums import PaymentStatus


#Functionality in Database

#Create payment in DB
def create_payment(db: Session, request: PaymentsBase, user_id: int):

    product = db_products.get_product(db, request.paid_product_id)
    if product.product_status is not ProductStatus.AVAILABLE:
        raise CanNotPayForReservedProduct()
    # if product.seller_id is user_id:
    #     raise CanNotPayForProduct()
    
    
    db_products.update_product_status_buyer(db, request.paid_product_id, user_id)
    new_payment = DbPayment(
        payment_amount = request.payment_amount,
        payment_method = request.payment_method,
        paid_product_id = request.paid_product_id
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

# return all payments if admin
def get_all_payments_admin(db: Session):
    return db.query(DbPayment).all()
    
#Return all Payments from DB
def get_all_payments(db: Session, user_id: int):
    payments = (
        db.query(DbPayment)
        .join(DbProduct, DbProduct.product_id == DbPayment.paid_product_id)
        .filter(or_(DbProduct.seller_id == user_id, DbProduct.buyer_id == user_id))
        .all()  
    )

    return payments


#Return  Payment from DB with specifiec ID
def get_payment(db: Session, id: int, user_id: int):
    payment = db.query(DbPayment).filter(DbPayment.payment_id==id).first()
    if not payment:
      raise PaymentNotFound()
    payment = (
    db.query(DbPayment)
    .join(DbProduct, DbProduct.product_id == DbPayment.paid_product_id)
    .filter(
        DbPayment.payment_id == id,  
        or_(DbProduct.seller_id == user_id, DbProduct.buyer_id == user_id)  
    )
    .first()  
     )
    if not payment:
        raise CanNotAccessPayment()

    return payment



#Update attributes in payments table
def update_payment_status(db: Session, id: int):
    payment = db.query(DbPayment).filter(DbPayment.payment_id == id)
    if not payment.first():
        raise PaymentNotFound()
    payment.update({
            DbPayment.payment_status: PaymentStatus.DONE
        })
    db.commit()
    product_id = (
    db.query(DbPayment.paid_product_id)
    .filter(DbPayment.payment_id == id)
    .scalar()  
)

    db.query(DbProduct).filter(DbProduct.product_id == product_id).update(
        {DbProduct.product_status: ProductStatus.SOLD}
    )
    db.commit()
    
    return payment


#Delete Payment from DB
def delete_payment(db: Session, id: int, user_id: int):
    payment = get_payment(db, id, user_id)
    if payment.payment_status != PaymentStatus.IN_PROGRESS:
        raise CanNotDeletePayment()
    db.delete(payment)
    db.commit()
    return