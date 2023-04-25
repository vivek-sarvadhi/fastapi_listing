from pydantic import BaseModel, Field, validator
from fastapi import Form, UploadFile
import os
from .models import Listing
from .database import get_db, SessionLocal


class AddListingSchema(BaseModel):
    name: str = Field(...,)
    category_id: int = Field(...,)
    brand_id: int = Field(...,)
    hsn_code: int = Field(None) 
    dimensions: str = Field(...,)
    price: float = Field(...,)
    image: UploadFile = Field(...,)

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        category_id: int = Form(...),
        brand_id: int = Form(...),
        hsn_code: int = Form(None),
        dimensions: str = Form(...,),
        price: int = Form(...,),
        image: UploadFile = Form(...,)):
        return cls(name=name,category_id=category_id,brand_id=brand_id,hsn_code=hsn_code,dimensions=dimensions,price=price,image=image)
    

class DisplayCategoryList(BaseModel):
    id: int
    name: str

class DisplayBrandList(BaseModel):
    id: int
    name: str

class DisplayListingSchema(BaseModel):
    id: int
    name : str
    category_id: int
    brand_id: int
    hsn_code: int = None
    dimensions: str
    price: float
    image: str = None
    category: DisplayCategoryList = None
    brand: DisplayBrandList = None
    
    class Config:
        orm_mode = True

    @validator('image')
    def pass_path(cls, value, values: dict):
        session = SessionLocal()
        current_dir = os.getcwd()
        product_obj = session.query(Listing).get(values['id'])
        if product_obj.image:
            return f"{current_dir}/api/media/{product_obj.image}"
        else:
            return None

    @validator('category')
    def category_name(cls, value, values: dict):
        session = SessionLocal()
        current_dir = os.getcwd()
        product_obj = session.query(Listing).get(values['id'])
        print("product_obj",product_obj)
        if product_obj.category.name:
            product_obj.category.name
        else:
            return None



class UpdateListingSchema(BaseModel):
    name: str = Field(None)
    category_id: int = Field(None)
    brand_id: int = Field(None)
    hsn_code: int = Field(None) 
    dimensions: str = Field(None)
    price: float = Field(None)
    image: UploadFile = Field(None)

    @classmethod
    def as_form(
        cls,
        name: str = Form(None),
        category_id: int = Form(None),
        brand_id: int = Form(None),
        hsn_code: int = Form(None),
        dimensions: str = Form(None),
        price: int = Form(None),
        image: UploadFile = Form(None)):
        return cls(name=name,category_id=category_id,brand_id=brand_id,hsn_code=hsn_code,dimensions=dimensions,price=price,image=image)
    

class DisplayBrandSchema(BaseModel):
    id: int
    name : str 
    
    class Config:
        orm_mode = True

