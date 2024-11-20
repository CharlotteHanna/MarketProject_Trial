from operator import or_
from sqlalchemy.orm.session import Session
from db.models import DbConversation, DbProduct

from exceptions import CanNotAccessConversation, CanNotDeleteConversationWithContent, ConversationNotFound




#Functionality in Database

#Create conversation in DB
def create_conversation(db: Session, potential_buyer_id: int, desired_product_id: int):
    
    new_conversation = DbConversation(
    potential_buyer_id = potential_buyer_id,
    desired_product_id = desired_product_id
    )

    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation

#Return all Conversations from DB
def get_all_conversations(db: Session, user_id: int):
 conversations =   db.query(DbConversation).outerjoin(DbProduct, DbConversation.desired_product_id == DbProduct.product_id).filter(or_(
            DbProduct.seller_id == user_id,              
            DbConversation.potential_buyer_id == user_id  
        )
    ).all()
 


 return conversations



#Return  Conversation from DB with specifiec ID
def get_conversation_by_id(db: Session, id: int, user_id: int):
 conversation = db.query(DbConversation).filter(DbConversation.conversation_id==id).first()
 if not conversation:
      raise ConversationNotFound()
 conversation = db.query(DbConversation).join(DbProduct, DbConversation.desired_product_id == DbProduct.product_id, isouter=True).filter(
        or_(
            DbProduct.seller_id == user_id,
            DbConversation.potential_buyer_id == user_id
        )
    ).filter(DbConversation.conversation_id == id).first()
 if not conversation:
   raise CanNotAccessConversation()

 return conversation
 

#Delete Conversation from DB
def delete_conversation(id: int, db: Session):
 conversation = db.query(DbConversation).filter(DbConversation.conversation_id==id).first()
 if conversation.messages:
   raise CanNotDeleteConversationWithContent()
 db.delete(conversation)
 db.commit()
 return 
 
