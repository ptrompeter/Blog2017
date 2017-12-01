"""Home and page non-specific views."""
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..forms import RegistrationForm
from ..models.user import User
from ..services.blog_record import BlogRecordService
from ..services.user import UserService


@view_config(route_name='home',
             renderer='Blog2017:templates/index.jinja2')
def index_page(request):
    """Default view."""
    page = int(request.params.get('page', 1))
    paginator = BlogRecordService.get_paginator(request, page)
    return {'paginator': paginator}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    """Handle login and logout requests and redirect the user."""
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
    return {}


@view_config(route_name='register',
             renderer='Blog2017:templates/register.jinja2')
def register(request):
    """Return a registration form on GET, submit new user on POST."""
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}


@view_config(route_name='api')
def check_api(request):
    """Return a string to a call to /api."""
    return Response('this api call returns a string.')

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_Blog2017_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
