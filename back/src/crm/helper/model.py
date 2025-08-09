from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()  

class Base(DeclarativeBase):
    __abstract__ = True  
    metadata = metadata