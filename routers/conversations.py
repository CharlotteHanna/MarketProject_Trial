from fastapi import APIRouter, Depends, status
from db.models import DbUser
from schemas import  ConversationDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_conversations
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/conversations',
    tags=['conversations']
)

@router.get('/',response_model=List[ConversationDisplay],  status_code=status.HTTP_200_OK)
def get_all_conversations(db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
      return db_conversations.get_all_conversations(db, current_user.user_id)
    
    
    #return Conversations with conditions
@router.get('/{id}',response_model=ConversationDisplay,  status_code=status.HTTP_200_OK)
def get_conversation(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
  return db_conversations.get_conversation_by_id(db, id, current_user.user_id) 

  
  
#Use Delete Conversation functionality from db_conversations file
@router.delete('/{id}',  status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
   db_conversations.get_conversation_by_id(db,id, current_user.user_id) 
   
   return db_conversations.delete_conversation(id, db)
  

