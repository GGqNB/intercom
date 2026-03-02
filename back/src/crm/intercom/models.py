from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func, Float
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import BYTEA, ARRAY

from src.crm.build.models import Entry
from src.crm.helper.model import Base

class Intercom(Base):
    __tablename__ = "intercom"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tech_name = Column(String, nullable = False)
    entry_id = Column(Integer, ForeignKey(Entry.id, ondelete='CASCADE'), nullable=False)
    # Relationship
    entry = relationship(Entry, passive_deletes=True)

