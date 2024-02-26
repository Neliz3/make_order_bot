from sqlalchemy import Column, Integer, String, Boolean
from .engine import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone = Column(String)


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String)
    price = Column(Integer, default=0)
    amount = Column(Integer, default=0)


class Carts(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    id_user = Column(Integer)
    id_product = Column(Integer)
    amount = Column(Integer, default=0)
    approval = Column(Boolean, default=False)
