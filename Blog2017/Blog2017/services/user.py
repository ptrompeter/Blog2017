"""Service for user authentication and authorization."""
from ..models.user import User


class UserService(object):
    """Handle User authorization and authentication requests."""

    @classmethod
    def by_name(cls, name, request):
        """Return a query with a single user identified by name."""
        return request.dbsession.query(User).filter(User.name == name).first()
