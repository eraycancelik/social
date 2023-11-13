from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(Text, nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

class Post(Base):
    __tablename__ = "posts"
    post_id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class Products(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True, nullable=False)
    product_name = Column(String, index=True, nullable=False)
    product_category = Column(String, nullable=False)
    product_price = Column(Integer, nullable=False)
    product_photo_url = Column(String, nullable=False)
    inventory = Column(Integer, server_default="100", nullable=False)
    is_sale = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.post_id",ondelete="CASCADE"),primary_key=True)

class Address(Base):
    __tablename__ = "addresses"
    address_id = Column(Integer, primary_key=True, nullable=False)
    address_type = Column(String, nullable=False)
    address_user_name = Column(String, nullable=False)
    address_user_surname = Column(String, nullable=False)
    address_user_phone = Column(String, nullable=False)
    address_city = Column(String, nullable=False)
    address_line = Column(String, nullable=False)
    zipcode = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"), nullable=False)
    customer = relationship('User')
