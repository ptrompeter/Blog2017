"""User Model."""
import datetime
from Blog2017.models.meta import Base
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
)


class User(Base):
    """Define a user model."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)
