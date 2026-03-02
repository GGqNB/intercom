from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func, Float
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import BYTEA, ARRAY
from src.crm.helper.model import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


# class Base(DeclarativeBase):
#     pass

# class TemplatePass(Base):
#     __tablename__ = "template_pass"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     width_mm = Column(Integer, nullable=False)
#     higth_mm = Column(Integer, nullable=False)
#     # ForeignKey
#     event_id = Column(Integer, ForeignKey(Events.id, ondelete='CASCADE'), nullable=False)
#     # Relationship
#     event = relationship(Events, passive_deletes=True)
#     blocks = relationship(Block, secondary="template_pass_has_blocks", backref="template_passes")
    
# class TemplatePassHasBlocks (Base):
#     __tablename__ = "template_pass_has_blocks"
#     id = Column(Integer, primary_key=True)
#     template_pass_id = Column(Integer,ForeignKey(TemplatePass.id,  ondelete='CASCADE'),  nullable=False)
#     block_id = Column(Integer,ForeignKey(Block.id,  ondelete='CASCADE'),  nullable=False)
    
# class TemplatePicture(Base):
#     tablename = "template_picture"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     width_mm = Column(Integer, nullable=False)
#     higth_mm = Column(Integer, nullable=False)
#     photo_url = Column(String, nullable=False)
#      # ForeignKey
#     event_id = Column(Integer, ForeignKey(Events.id,  ondelete='CASCADE'),  nullable=False)
#     # Relationship
#     event = relationship(Events,  passive_deletes=True)