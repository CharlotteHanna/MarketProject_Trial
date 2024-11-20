from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db import db_conversations
from db.models import DbMessage, DbConversation, DbProduct
from exceptions import MessageNotFound
from schemas import MessageBase






#Functionality in Database

#Create message in DB
def create_message(db:Session, request: MessageBase, conversation_id: Optional[int], desired_product_id: Optional[int], sender_id : int):


    product = (
        db.query(DbProduct)
        .filter(
            DbProduct.product_id == desired_product_id,
            DbProduct.seller_id == sender_id
        )
        .first()
    )
    if product: 
      return None



#  check if we are creating a new conversation
    if not conversation_id:
  
        new_conversation = db_conversations.create_conversation(db, sender_id, desired_product_id)
        new_message = DbMessage(
        conversation_id=new_conversation.conversation_id,
        sender_id = sender_id,
        content =request.content
       )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
 
# check if current user allowed to participate in a conversation
    db_conversations.get_conversation_by_id(db, conversation_id, sender_id)


    new_message = DbMessage(
      conversation_id=conversation_id,
      sender_id = sender_id,
      content =request.content
 )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

# def get_messages_by_conversation(db:Session, conversation_id:int):
#  conversation =db.query(DbConversation).filter(DbConversation.id==conversation_id).first()
#  if not conversation:
#   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="Conversation not found")
 
#  messages = db.query(DbMessage).filter(DbMessage.conversation_id==conversation_id).order_by(DbMessage.timestamp).all()
#  return messages


# def get_message_by_id(db:Session, message_id:int):
#  message = db.query(DbMessage).filter(DbMessage.id ==message_id).first()
#  if not message:
#   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="Message not found")
#  return message



# check if message exists
def message_exists(db: Session, id: str):
    message = db.query(DbMessage).filter(DbMessage.message_id == id).first()
    if not message:
       raise MessageNotFound()
    return message



#Delete Message from DB
def delete_message(db: Session, id: int):
 
 message = db.query(DbMessage).filter(DbMessage.message_id == id).first()
 db.delete(message)
 db.commit()
 return



