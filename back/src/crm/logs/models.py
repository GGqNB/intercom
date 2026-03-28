from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func, Float
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import BYTEA, ARRAY

from src.crm.build.models import Entry
from src.crm.helper.model import Base

class CallLog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # call_created / call_failed / call_sent
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    house_id = Column(Integer, nullable=False)
    flat = Column(Integer, nullable=False)
    photo_url = Column(String, nullable=True)
    indentifier = Column(String, nullable=True)

    # Тип события

    # Время события

    # Связь с пользователем
    # user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    # user = relationship("Users")

    # Данные вызова

    # chat_id = Column(String, nullable=True)
    # max_id = Column(String, nullable=True)

    # device_identifier = Column(String, nullable=True)
    # Фото
    # Статус
    #status = Column(String, nullable=False)  # created / sent / failed