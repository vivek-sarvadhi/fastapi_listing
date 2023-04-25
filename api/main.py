from fastapi import FastAPI
from .routers import seed_data, listing
from .models import Brand
from sqlalchemy import event
from .database import Base, engine

# event.listen(Brand.__table__, 'after_create', seed_data.initialize_table)

app = FastAPI()

# @app.on_event("startup")
# def configure():
#     print("Starting up...")
#     Base.metadata.create_all(bind=engine)
app.include_router(seed_data.router)
app.include_router(listing.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

