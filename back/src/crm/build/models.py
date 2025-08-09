from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func, Float
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import BYTEA, ARRAY
from sqlalchemy import MetaData
from src.crm.location.models import City
from src.crm.helper.model import Base

class House(Base):
    __tablename__ = "house"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    geo_adress = Column(String, nullable = False)
    flat_count = Column(Integer, nullable = False)
    city_id = Column(Integer, ForeignKey(City.id, ondelete='CASCADE'), nullable=False)
    # Relationship
    city = relationship(City, passive_deletes=True)


class Entry(Base):
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    flat_first = Column(Integer, nullable = False)
    flat_last = Column(Integer, nullable = False)
    house_id = Column(Integer, ForeignKey(House.id, ondelete='CASCADE'), nullable=False)
    # Relationship
    house = relationship(House, passive_deletes=True)

# class Flat(Base):
#     _tablename__ = "entry"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     ext_number = Column(String, nullable=False)
#     ext_number = Column(String, nullable=False)


