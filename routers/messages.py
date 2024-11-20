
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from db.models import DbUser
from exceptions import CanNotStartConversation, FillParameters, MessageNotFound
from schemas import MessageBase, MessageDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_messages
from auth.oauth2 import get_current_user



router = APIRouter(
prefix='/messages',
tags=['messages']
)



#Use Create Message functionality from db_messages file
@router.post('/', response_model=MessageDisplay,  status_code=status.HTTP_200_OK)
def create_message(request: MessageBase , conversation_id: Optional[int] = None, desired_product_id: Optional[int] = None, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if not conversation_id and not desired_product_id:
        raise FillParameters()
    message=  db_messages.create_message(db, request, conversation_id, desired_product_id, current_user.user_id)
    if not message:
        raise CanNotStartConversation()
    return message



#Use Delete Message functionality from db_messages file
@router.delete('/{id}',  status_code=status.HTTP_204_NO_CONTENT)

def delete_message(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
  
  message = db_messages.message_exists(db, id)
  if message.sender_id != current_user.user_id:
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have enough permissions to perform this action')
  message = db_messages.delete_message(db, id)
 
  
