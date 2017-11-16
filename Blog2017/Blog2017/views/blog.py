from pyramid.view import view_config


@view_config(route_name='blog',
             renderer='Blog2017:templates/view_blog.jinja2')
def blog_view(request):
    """This route returns the basic blog view."""
    return {}


@view_config(route_name='blog_action', match_param='action=create',
             renderer='Blog2017:templates/edit_blog.jinja2')
def blog_create(request):
    """This route handles requests to add new records."""
    return {}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='Blog2017:templates/edit_blog.jinja2')
def blog_update(request):
    """This route handles requests to update records."""
    return {}
