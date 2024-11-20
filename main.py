from fastapi import FastAPI
from db.database import engine, SessionLocal
from db import  models
from db.initialize_first_admin import initialize_first_admin
from routers import conversations, messages, payments, products, users, images, categories, ratings
from auth import authentication
from fastapi.staticfiles import StaticFiles
from exceptions import register_all_errors

app = FastAPI()



@app.on_event("startup")
def startup_event():
    """
    it creates the first admin
    """
    with SessionLocal() as db:  # starts a database connection. We used with and it ends process after works.
        initialize_first_admin(db)


register_all_errors(app)


app.include_router(ratings.router)
app.include_router(authentication.router)
app.include_router(images.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(conversations.router)
app.include_router(messages.router)
app.include_router(payments.router)

# app.include_router(authentication.router)





# Create the database tables  
models.Base.metadata.create_all(engine)


app.mount("/images", StaticFiles(directory="images"), name="images")





