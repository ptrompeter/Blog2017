"""Model for blog records."""
import datetime
from Blog2017.models.meta import Base
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
)


class BlogRecord(Base):
    """Define the model for blog entries."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
