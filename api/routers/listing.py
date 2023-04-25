from sqlalchemy.orm import Session, joinedload
from sqlalchemy import not_
from ..models import Listing, Category, Brand
from fastapi import Depends, APIRouter, status, UploadFile, Response, File, HTTPException
from ..schemas import AddListingSchema, DisplayListingSchema, UpdateListingSchema, DisplayBrandSchema
import pandas as pd
import numpy as np
from ..database import get_db, engine
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
import uuid, os
router = APIRouter()
# Imagedir = "image/"

@router.post('/add_listing', status_code=status.HTTP_201_CREATED)
def create_listing(response: Response, payload: AddListingSchema = Depends(AddListingSchema.as_form), db: Session = Depends(get_db)):
    listing_name = payload.name.upper()
    existing_listing = db.query(Listing).filter(Listing.name == listing_name).first()
    if existing_listing:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'success':False, 'message':'Cannot create listing listing ID already available.'}
    brand_id = db.query(Brand).get(payload.brand_id)
    if brand_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'success':False, 'message':'Cannot create listing brand ID is missing.'}
    if brand_id.category_id == payload.category_id:
        current_dir = os.getcwd()
        current_dirr = f"{current_dir}/api/media/{payload.image.filename}"
        contents = payload.image.file.read()
        with open(f"{current_dirr}", "wb") as f:
            f.write(contents)
        new_post = Listing(name=listing_name, category_id=payload.category_id, brand_id=payload.brand_id, hsn_code=payload.hsn_code, dimensions=payload.dimensions, price=payload.price, image=payload.image.filename)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {'success':True, 'message':'Listing has been created successfully.'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'success':False, 'message':'Cannot create listing category ID is missing.'}


@router.get('/display_listing')
def display_listing(response: Response, db: Session = Depends(get_db), search: Optional[str] = ""):
    response_datas = db.query(Listing).filter(Listing.name.contains(search)).all()
    listing_data = []
    for response_data in response_datas:
        category_name = db.query(Category).get(response_data.category_id)
        brand_name = db.query(Brand).get(response_data.brand_id)
        current_dir = os.getcwd()
        image = f"{current_dir}/api/media/{response_data.image}"
        data = {
            "id":response_data.id,
            "name":response_data.name,
            "category_name":category_name.name,
            "brand_name":brand_name.name,
            "hsn_code":response_data.hsn_code,
            "dimensions":response_data.dimensions,
            "price":response_data.price,
            "image":image
        }
        listing_data.append(data)
    if not listing_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'success':False, 'message':'Listing data not found.'}
    return {'success':True, 'message':'listing display successfully.', "result":listing_data}
    # response_data = db.query(Listing).options(joinedload(Listing.category),joinedload(Listing.brand)).filter(Listing.name.contains(search)).all()
    # return jsonable_encoder(response_data)
    # return {'success':True, 'message':'listing create successfully.', "result":jsonable_encoder(response_data)}


@router.get("/display_listing/{listing_id}")
def get_posts_detail(response: Response, listing_id: int, db: Session = Depends(get_db)):
    response_data = db.query(Listing).filter_by(id=listing_id).first()
    if not response_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'success':False, 'message':'Listing data not found.'}
    listing_data = []
    category_name = db.query(Category).get(response_data.category_id)
    brand_name = db.query(Brand).get(response_data.brand_id)
    current_dir = os.getcwd()
    image = f"{current_dir}/api/media/{response_data.image}"
    data = {
        "id":response_data.id,
        "name":response_data.name,
        "category_name":category_name.name,
        "brand_name":brand_name.name,
        "hsn_code":response_data.hsn_code,
        "dimensions":response_data.dimensions,
        "price":response_data.price,
        "image":image
    }
    listing_data.append(data)
    return {'success':True, 'message':'listing display successfully.', "result":listing_data}
    # response_data = db.query(Listing).options(joinedload(Listing.category),joinedload(Listing.brand)).filter(Listing.id==listing_id).first()
    # if not response_data:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {listing_id} not found")
    # return jsonable_encoder(response_data)


@router.put("/update_listing/{listing_id}")
def update_listing(response: Response, listing_id: int, update_listing: UpdateListingSchema = Depends(UpdateListingSchema.as_form), db: Session = Depends(get_db)):
    listing_name = update_listing.name.upper()
    response_data = db.query(Listing).filter(Listing.id == listing_id).first()
    if response_data is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'success':False, 'message':f'Cannot update listing the listing with ID {listing_id} does not exist.'}
    existing_listing = db.query(Listing).filter(Listing.name == listing_name,not_(Listing.id == listing_id)).first()
    if existing_listing:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'success':False, 'message':'Cannot update listing listing name already available.'}
    brand_id = db.query(Brand).get(update_listing.brand_id)
    if brand_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'success':False, 'message':'Cannot update listing brand ID is missing.'}
    print("brand_id.category_id",brand_id)
    if brand_id.category_id == update_listing.category_id:
        current_dir = os.getcwd()
        current_dirr = f"{current_dir}/api/media/{update_listing.image.filename}"
        contents = update_listing.image.file.read()
        with open(f"{current_dirr}", "wb") as f:
            f.write(contents)
        response_data.name = listing_name
        response_data.category_id = update_listing.category_id
        response_data.brand_id = update_listing.brand_id
        response_data.hsn_code = update_listing.hsn_code
        response_data.dimensions = update_listing.dimensions
        response_data.price = update_listing.price
        response_data.image = update_listing.image.filename
        db.commit()
        return {'success':True, 'message':'Listing has been update successfully.'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'success':False, 'message':'Cannot update listing category ID is missing.'}


@router.delete("/listing_delete/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(response: Response, listing_id: int, db: Session = Depends(get_db)):
    product_query = db.query(Listing).filter(Listing.id == listing_id)
    product = product_query.first()
    if product == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'success':False, 'message':'Listing data not found.'}
    product_query.delete(synchronize_session=False)
    db.commit()
    return {'success':False, 'message':'Listing delete successfully.'}

@router.get("/display_brand_detail_category_wise")
def get_brand_detail_category_wise(response: Response, category_id: int, db: Session = Depends(get_db)):
    response_datas = db.query(Brand).filter_by(category_id=category_id)
    brand_data = []
    for response_data in response_datas:
        data = {
            "id":response_data.id,
            "name":response_data.name
        }
        brand_data.append(data)
    if not brand_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'success':False, 'message':f'Brand with category id {category_id} not found.'}
    return {'success':True, 'message':'listing display successfully.', "result":brand_data}