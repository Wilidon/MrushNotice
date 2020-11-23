from sqlalchemy import (Boolean, Column, Integer, String,
                        DateTime, func)

from .database import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, primary_key=True)
    username = Column(String(32))
    first_name = Column(String(64))
    last_name = Column(String(64))
    notice = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Threads(Base):
    __tablename__ = "threads"
    __table_args__ = {"schema": "public"}

    thread_id = Column(Integer, primary_key=True)
