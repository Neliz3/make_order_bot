from sqlalchemy import Column, Integer, String
from .engine import Base


#   Table to store all users
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone = Column(String)
