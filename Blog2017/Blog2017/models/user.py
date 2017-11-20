"""User Model."""
import datetime
from Blog2017.models.meta import Base
from passlib.apps import custom_app_context as blog2017_pwd_context
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

    def verify_password(self, password):
        """Verify user password, converts plaintext to secure hashes."""
        if password == self.password:
            self.set_password(password)
        return blog2017_pwd_context.verify(password, self.password)

    def set_password(self, password):
        """Set the password attribute on the User object."""
        password_hash = blog2017_pwd_context.encrypt(password)
        self.password = password_hash
