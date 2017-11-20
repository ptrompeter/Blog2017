"""Contains forms."""
from wtforms import Form, StringField, TextAreaField, validators
from wtforms import IntegerField, PasswordField
from wtforms.widgets import HiddenInput

strip_filter = lambda x: x.strip() if x else None

class BlogCreateForm(Form):
    """Create a form for new blog entries."""
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    body = TextAreaField('Contents', [validators.Length(min=1)],
                         filters=[strip_filter])


class BlogUpdateForm(BlogCreateForm):
    """Create form to insert hidden id when editing a post."""

    id = IntegerField(widget=HiddenInput())


class RegistrationForm(Form):
    """Create a form for new user registration."""

    username = StringField('Username', [validators.Length(min=1, max=255)],
                           filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=3)])
