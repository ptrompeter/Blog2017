from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config
from ..models.blog_record import BlogRecord
from ..services.blog_record import BlogRecordService


@view_config(route_name='blog',
             renderer='Blog2017:templates/view_blog.jinja2')
def blog_view(request):
    """Return the basic blog view."""
    blog_id = int(request.matchdict.get('id', -1))
    entry = BlogRecordService.by_id(blog_id, request)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='blog_action', match_param='action=create',
             renderer='Blog2017:templates/edit_blog.jinja2')
def blog_create(request):
    """Handle requests to add new records."""
    return {}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='Blog2017:templates/edit_blog.jinja2')
def blog_update(request):
    """This route handles requests to update records."""
    return {}
