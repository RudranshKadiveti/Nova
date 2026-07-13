from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Sender(Base):
    __tablename__ = "senders"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True) # e.g., "telegram", "gmail"
    identifier = Column(String, unique=True, index=True) # email or phone number/username
    action_rule = Column(String, default="ask") # "ask", "auto-sync", "ignore"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, index=True)
    title = Column(String)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    location = Column(String, nullable=True)
    status = Column(String, default="pending") # "pending", "synced"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
