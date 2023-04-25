from sqlalchemy.orm import Session
# from api import models, database
from ..models import Category, Brand
from fastapi import Depends, APIRouter
from ..database import get_db, engine
import subprocess
router = APIRouter()

def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()

def seed_category_data(db: Session):
    initial_data = [
        {"name": "FABRIC"},
        {"name": "FORMALWEAR"},
        {"name": "KIDSWEAR"},
        {"name": "LUXURY FORMALWEAR"},
        {"name": "GENERAL"},
    ]
    # Loop through initial data and create database objects
    for data in initial_data:
        print(data)
        existing_item = get_category_by_name(db, data['name'])
        if not existing_item:
            db_item = Category(**data)
            db.add(db_item)

    # Commit changes to the database
    db.commit()

def get_brand_by_name(db: Session, name: str):
    return db.query(Brand).filter(Brand.name == name).first()

def seed_brand_data(db: Session):
    initial_data = [
        {
            "name": "RAYMOND",
            "category_id": 9
        },
        {
            "name": "VIMAL",
            "category_id": 9
        },
        {
            "name": "SIYARAM",
            "category_id": 9
        },
        {
            "name": "GWALIOR",
            "category_id": 9
        },
        {
            "name": "ARROW",
            "category_id": 10
        },
        {
            "name": "PARK AVENUE",
            "category_id": 10
        },
        {
            "name": "PETER ENGLAND",
            "category_id": 10
        },
        {
            "name": "ALLEN SOLLY",
            "category_id": 10
        },
        {
            "name": "JOHN PLAYERS",
            "category_id": 10
        },
        {
            "name": "VAN HEUSEN",
            "category_id": 10
        },
        {
            "name": "ZODIAC",
            "category_id": 10
        },
        {
            "name": "LOUIS PHILIPPE",
            "category_id": 10
        },
        {
            "name": "OXEMBERG",
            "category_id": 10
        },
        {
            "name": "LILIPUT",
            "category_id": 11
        },
        {
            "name": "CANALI",
            "category_id": 12
        },
        {
            "name": "RAMRAJ",
            "category_id": 13
        }
    ]
    # Loop through initial data and create database objects
    for data in initial_data:
        existing_item = get_brand_by_name(db, data['name'])
        if not existing_item:
            db_item = Brand(**data)
            db.add(db_item)
    # Commit changes to the database
    db.commit()


@router.get('/add_seeder')
def add_seeder():
    db = Session(engine)
    seed_category_data(db)
    seed_brand_data(db)
    return {'success':True, 'message':'add data successfully.'}


@router.get("/apply_migrate")
def generate_migration(message: str):
    result_generate = subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], capture_output=True)
    generate_output = result_generate.stdout.decode("utf-8")
    result_upgrade = subprocess.run(["alembic", "upgrade", "head"], capture_output=True)
    upgrade_output = result_upgrade.stdout.decode("utf-8")
    if result_generate.returncode != 0 and result_upgrade.returncode != 0:
        return {"status": "error", "generate_message": generate_output, "upgrade_message":upgrade_output}
    return {"status": True, "message": "migration run successfully"}


# @router.post("/apply_migrate")
# async def apply_migrations():
#     result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True)
#     output = result.stdout.decode("utf-8")
#     if result.returncode != 0:
#         return {"status": "error", "message": output}
#     else:
#         return {"status": "success", "message": output}
