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
from webhelpers2.date import distance_of_time_in_words
from webhelpers2.text import urlify


class BlogRecord(Base):
    """Define the model for blog entries."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def slug(self):
        """Create a URL slug to be inserted into paths."""
        return urlify(self.title)

    @property
    def created_in_words(self):
        """Return a string describing how long ago an entry was created."""
        return distance_of_time_in_words(self.created,
                                         datetime.datetime.utcnow())
