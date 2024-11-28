from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, logger, status
from sqlalchemy.orm import Session
from db.database import get_db
from enums import ProductStatus
from exceptions import ProductNotFound
from schemas import RatingAggregation, RatingBase, RatingDisplay, RatingUpdate, RatingsResponse
from db import db_ratings
from auth.oauth2 import get_current_user
from db.models import DbProduct, DbRating, DbUser

router = APIRouter(
    prefix='/ratings',
    tags=['ratings']
)

@router.post('/', response_model=RatingDisplay)
def create_rating(
    request: RatingBase,
    db: Session = Depends(get_db),
    current_user:DbUser = Depends(get_current_user)):
    
    #Retrieve the  product without using the current user
    product = db.query(DbProduct).filter(DbProduct.product_id == request.product_id).first()
    if not product:
        raise ProductNotFound()

    # Perform security checks after data retrieval

    # Check if the product has been sold
    if product.product_status is not ProductStatus.SOLD:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only rate sold products")

    # Ensure the user being rated is involved in the transaction
    if request.ratee_id not in [product.seller_id, product.buyer_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user being rated is not involved in this transaction"  
        )

    # Ensure the rater is involved in the transaction
    if request.rater_id not in [product.seller_id, product.buyer_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user giving the rating is not involved in this transaction"
        )

    # Prevent a user from rating themselves
    if request.ratee_id == request.rater_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot rate yourself"
        )

    # Ensure the rater is the current user
    if request.rater_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to rate on behalf of another user"
        )

    # Check if the rater has already rated this transaction
    existing_rating = db.query(DbRating).filter(
        DbRating.product_id == request.product_id,
        DbRating.rater_id == request.rater_id
    ).first()
    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have already rated this transaction"
        )

    # Determine if this is a seller or buyer rating
    is_seller_rating = (request.rater_id == product.buyer_id)

    # Create the rating
    new_rating = db_ratings.create_rating(
        db=db,
        request=request,
        is_seller_rating=is_seller_rating
    )

    return new_rating

@router.get('aggregations', response_model=List[RatingAggregation])  
def get_ratings_aggregation(  
    user_id: int = Query(..., description="User ID to aggregate ratings for"),  
    db: Session = Depends(get_db)  
):  
    aggregation = db_ratings.get_ratings_aggregation(db, user_id=user_id)  
    if not aggregation:  
        raise HTTPException(status_code=404, detail="No ratings found for this user")  
    return [aggregation]

@router.get('/', response_model=RatingsResponse)  
def get_ratings_by_ratee(  
    ratee_id: Optional[int] = Query(None, description="Filter by ratee ID"),  
    product_id: Optional[int] = Query(None, description="Filter by product ID"),  
    skip: int = Query(0, ge=0, description="Number of records to skip"),  
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),   
    db: Session = Depends(get_db)  
):   
    # try:  
        # Get ratings and total  
        ratings, total_ratings = db_ratings.get_ratings_by_ratee(  
            db, ratee_id=ratee_id, product_id=product_id, skip=skip, limit=limit  
        )  
        
        # Get average ratings  
        average_seller_rating, average_buyer_rating = (None, None)  
        if ratee_id:  
            average_seller_rating, average_buyer_rating = db_ratings.calculate_average_ratings(  
                db, ratee_id=ratee_id  
            )  
        
        # Construct  the response dictionary  
        response_data = {  
            "ratings": ratings,  
            "average_seller_rating": average_seller_rating,  
            "average_buyer_rating": average_buyer_rating,  
            "total_ratings": total_ratings  
        }  
        
        return response_data
    
    
@router.get('/{id}', response_model=RatingDisplay)  
def get_rating_by_id(  
    id: int,  
    db: Session = Depends(get_db)  
):  
    rating = db_ratings.get_rating_by_id(db, id)  
    if not rating:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")  
    return rating 



@router.put('/{id}', response_model=RatingDisplay)  
def update_rating(  
    id: int,  
    request: RatingUpdate,  
    db: Session = Depends(get_db),  
    current_user: DbUser = Depends(get_current_user)  
):  
    rating = db_ratings.get_rating_by_id(db, id)  
    if not rating:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")  

    if rating.rater_id != current_user.user_id:  
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this rating")  

    updated_rating = db_ratings.update_rating(db, id, request)  
    return updated_rating

@router.delete('/{id}', status_code=204)  
def delete_rating(  
    id: int,  
    db: Session = Depends(get_db),  
    current_user: DbUser = Depends(get_current_user)  
):  
    # Retrieve the rating by its ID  
    rating = db_ratings.get_rating_by_id(db, id)  
    if not rating:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")  

    # Check if the current user is the one who created the rating  
    if rating.rater_id != current_user.user_id:  
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this rating")  

    # Proceed to delete the rating since the user is authorized  
    db_ratings.delete_rating(db, id)  
    return  # No content to return for a 204 response

