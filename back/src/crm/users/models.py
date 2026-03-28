from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, UniqueConstraint, func, Float
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import BYTEA, ARRAY

from src.crm.build.models import House
from src.crm.helper.model import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_id = Column(String, nullable=False)
    max_id = Column(String, nullable=False)
    flat = Column(Integer, nullable=False)
    flat_stown = Column(Integer, nullable=False)
    house_id = Column(Integer, ForeignKey("house.id", ondelete='CASCADE'), nullable=False)

    house = relationship(House, passive_deletes=True)

    __table_args__ = (
        UniqueConstraint(
            "max_id",
            "house_id",
            "flat",
            name="uq_user_unique_flat"
        ),
    )
