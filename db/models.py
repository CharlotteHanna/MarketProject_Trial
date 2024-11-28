from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Enum,Float, ForeignKey, Integer, String, Text  # noqa: F401
from db.database import Base
from sqlalchemy.orm import relationship

from enums import PaymentStatus, ProductStatus

# Rating Table
class DbRating(Base):  
    __tablename__ = "ratings"  
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    rating = Column(Integer)  # 1-5 rating  
    review = Column(String, nullable=True)  # Optional review text  
    is_seller_rating = Column(Boolean)  # True if rating is for seller, False if for buyer    , nullable=False, default=False) 
    ratee_id = Column(Integer, ForeignKey("users.user_id"))  # User receiving the rating  
    rater_id = Column(Integer, ForeignKey("users.user_id"))  # User giving the rating  
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  
    product = relationship("DbProduct", foreign_keys=[product_id])
    user = relationship("DbUser", foreign_keys=[ratee_id], back_populates="ratings")
    creator = relationship("DbUser", foreign_keys=[rater_id], back_populates="ratings_given")

#  User Table
class DbUser(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True) #primary key
    username = Column(String, unique=True)  # Unique username  
    email = Column(String, unique=True)     # Unique email  
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    sold_product = relationship("DbProduct", primaryjoin="DbUser.user_id==DbProduct.seller_id")
    bought_product = relationship("DbProduct", primaryjoin="DbUser.user_id==DbProduct.buyer_id")
    conversations = relationship("DbConversation", back_populates="potential_buyer")
    messages = relationship("DbMessage", back_populates="sender")
    ratings = relationship("DbRating", foreign_keys=[DbRating.ratee_id], back_populates="user")
    ratings_given = relationship("DbRating", foreign_keys=[DbRating.rater_id], back_populates="creator")
    @property  
    def average_seller_rating(self):  
        if not self.ratings:  
            return None  
        seller_ratings = [r.rating for r in self.ratings if r.is_seller_rating]  
        return round(sum(seller_ratings) / len(seller_ratings), 2) if seller_ratings else None  

    @property  
    def average_buyer_rating(self):  
        if not self.ratings:  
            return None  
        buyer_ratings = [r.rating for r in self.ratings if not r.is_seller_rating]  
        return round(sum(buyer_ratings) / len(buyer_ratings), 2) if buyer_ratings else None  

    @property  
    def total_ratings(self):  
        return len(self.ratings) 



# Product Table
class DbProduct(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True) #primary key
    product_name = Column(String)
    description = Column(String)
    price = Column(Integer)  # Price is in cents   
    image_url = Column(String)
    product_category_id = Column(Integer, ForeignKey('categories.category_id'))
    product_status = Column(Enum(ProductStatus), default=ProductStatus.AVAILABLE)
    seller_id = Column(Integer, ForeignKey('users.user_id'))  # FK for seller
    buyer_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)  # FK for buyer, allow buyer_id to be null
    seller = relationship("DbUser", foreign_keys=[seller_id], back_populates="sold_product")
    buyer = relationship("DbUser",  foreign_keys=[buyer_id], back_populates="bought_product")
    product_category = relationship("DbCategory",  foreign_keys=[product_category_id], back_populates="product")
    product_conversation = relationship("DbConversation",  back_populates="product")
    payments = relationship("DbPayment",  back_populates="paid_product")



# Category Table
class DbCategory(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True) #primary key
    category_name = Column(String)
    product = relationship("DbProduct", back_populates="product_category")



# Conversation Table
class DbConversation(Base):
    __tablename__ = "conversations"
    conversation_id = Column(Integer, primary_key=True, index=True)
    potential_buyer_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)  
    desired_product_id = Column(Integer, ForeignKey("products.product_id"), nullable=True) 
    potential_buyer = relationship("DbUser", foreign_keys=[potential_buyer_id], back_populates="conversations")  
    product = relationship("DbProduct", foreign_keys=[desired_product_id], back_populates="product_conversation")
    messages = relationship("DbMessage",  back_populates="conversation")



# Message table
class DbMessage(Base):
    __tablename__ = "messages"
    message_id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.conversation_id"), nullable=True)
    sender_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sender = relationship("DbUser",  foreign_keys=[sender_id], back_populates="messages")
    conversation = relationship("DbConversation",  foreign_keys=[conversation_id], back_populates="messages")

# Payment Table
class DbPayment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    paid_product_id = Column(Integer,  ForeignKey("products.product_id"))
    payment_amount = Column(Integer) 
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.IN_PROGRESS)
    payment_method = Column(String)
    paid_product = relationship("DbProduct",  foreign_keys=[paid_product_id], back_populates="payments")

    #  paid_product = relationship("DbProduct",  foreign_keys=[paid_product_id], back_populates="payments")