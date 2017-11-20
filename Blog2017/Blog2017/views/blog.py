"""Contains views for displaying, creating, and updating blog entries."""
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config
from ..forms import BlogCreateForm, BlogUpdateForm
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
             renderer='Blog2017:templates/edit_blog.jinja2',
             permission='create')
def blog_create(request):
    """Display blog entry form.  If POST and valid, update DB."""
    entry = BlogRecord()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        request.dbsession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='Blog2017:templates/edit_blog.jinja2',
             permission='create')
def blog_update(request):
    """Display blog entry data in form; if POST and valid, update entry."""
    blog_id = int(request.params.get('id', -1))
    entry = BlogRecordService.by_id(blog_id, request)
    if not entry:
        return HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        del form.id  # SECURITY: prevent overwriting of primary key
        form.populate_obj(entry)
        return HTTPFound(
            location=request.route_url('blog', id=entry.id, slug=entry.slug))
    return {'form': form, 'action': request.matchdict.get('action')}

# TODO: Replace form.populate_obj with BlogRecord model method? Sloppy ATM.
