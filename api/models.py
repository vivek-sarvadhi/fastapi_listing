from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, UniqueConstraint, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
# from sqlalchemy_utils import URLType


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#     phone_number = Column(String)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    category = relationship("Category", backref='category_brand')


class Listing(Base):
    __tablename__ = 'listing'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.id', ondelete="CASCADE"), nullable=False)
    hsn_code = Column(Integer, nullable=True)
    # data = Column(Integer, nullable=True)
    # data1 = Column(Integer, nullable=True)
    # data2 = Column(Integer, nullable=True)
    dimensions = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    image = Column(String, nullable=True)
    category = relationship("Category", backref='category_listing')
    brand = relationship("Brand", backref='brand_listing')
