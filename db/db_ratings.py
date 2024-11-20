from typing import List, Optional, Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models import DbRating, DbProduct
from schemas import RatingBase
from fastapi import HTTPException
from sqlalchemy import func  
from schemas import RatingAggregation  


def create_rating(
    db: Session,
    request: RatingBase,
    is_seller_rating: bool
):
    new_rating = DbRating(
        product_id=request.product_id,
        ratee_id=request.ratee_id,
        rater_id=request.rater_id,
        rating=request.rating,
        review=request.review,
        is_seller_rating=is_seller_rating
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

def get_ratings_aggregation(db: Session, user_id: int):  
    avg_rating = db.query(func.avg(DbRating.rating)).filter(DbRating.ratee_id == user_id).scalar()  
    avg_seller_rating, avg_buyer_rating = calculate_average_ratings(db, ratee_id=user_id)  # Get both averages  
    rating_count = db.query(func.count(DbRating.id)).filter(DbRating.ratee_id == user_id).scalar()  

    if avg_rating is None or rating_count == 0:  
        return None  

    return RatingAggregation(  
        user_id=user_id,  
        average_rating=avg_rating,  
        average_seller_rating=avg_seller_rating,  # Include seller average  
        average_buyer_rating=avg_buyer_rating,    # Include buyer average  
        rating_count=rating_count  
    )

def get_ratings_by_ratee(  
    db: Session,  
    ratee_id: Optional[int] = None,  
    product_id: Optional[int] = None,
    skip: int = 0,
    limit:int = 10
) -> Tuple[List[DbRating], int]:
    query = db.query(DbRating)  
    if ratee_id:  
        query = query.filter(DbRating.ratee_id == ratee_id)  
    if product_id:  
        query = query.filter(DbRating.product_id == product_id)  
    total = query.count()  
    ratings = query.offset(skip).limit(limit).all()  
    return ratings, total  

def calculate_average_ratings(db: Session, ratee_id: Optional[int] = None) -> Tuple[Optional[float], Optional[float]]:  
    """  
    Calculate average seller and buyer ratings for a given ratee_id.  
    Returns a tuple of (average_seller_rating, average_buyer_rating).  
    """  
    if not ratee_id:  
        return None, None  

    # Calculate average seller rating  
    avg_seller = db.query(func.avg(DbRating.rating)).filter(  
        DbRating.ratee_id == ratee_id,  
        DbRating.is_seller_rating == True  
    ).scalar()  

    # Calculate average buyer rating  
    avg_buyer = db.query(func.avg(DbRating.rating)).filter(  
        DbRating.ratee_id == ratee_id,  
        DbRating.is_seller_rating == False  
    ).scalar()  

    # Round the averages to two decimal places if they are not None  
    avg_seller = round(avg_seller, 2) if avg_seller is not None else None  
    avg_buyer = round(avg_buyer, 2) if avg_buyer is not None else None  

    return avg_seller, avg_buyer

def get_rating_by_id(db: Session, id: int):  
    return db.query(DbRating).filter(DbRating.id == id).first()


def update_rating(db: Session, id: int, request: RatingBase):  
    rating = db.query(DbRating).filter(DbRating.id == id).first()  
    if rating:  
        rating.rating = request.rating  
        rating.review = request.review  
        db.commit()  
        db.refresh(rating)  
    return rating

def delete_rating(db: Session, id: int):  
    rating = db.query(DbRating).filter(DbRating.id == id).first()  
    if rating:  
        db.delete(rating)  
        db.commit()