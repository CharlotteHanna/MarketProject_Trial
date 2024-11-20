from sqlalchemy.orm import Session
from db.hash import Hash
from db.models import DbUser

def initialize_first_admin(db: Session):
    """
    if there is no admin in the system, create a new one.
    """
    admin_exists = db.query(DbUser).filter(DbUser.is_admin == True).first()
    if not admin_exists:
        first_admin = DbUser(
            username="admin",
            email="admin@example.com",
            password=Hash.bcrypt("admin123"),  
            is_admin=True
        )
        db.add(first_admin)
        db.commit()
        db.refresh(first_admin)