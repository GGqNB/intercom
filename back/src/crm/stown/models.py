from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.crm.build.models import House
from src.crm.helper.model import Base




class SFlat(Base):
    __tablename__ = "sflat"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    ext_number = Column(String, nullable=True)

    house_id = Column(
        Integer,
        ForeignKey("house.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationship
    house = relationship(
        "House",                
        back_populates="sflat",
        passive_deletes=True
    )
