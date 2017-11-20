"""Basic authentication scheme."""
from pyramid.security import Allow, Everyone, Authenticated


class BlogRecordFactory(object):
    """Create a context factory to handle authentication."""

    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'), ]

    def __init__(self, request):
        """Handle linter error."""
        pass
