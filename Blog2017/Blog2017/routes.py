"""Routes for blog access and login."""


def includeme(config):
    """Included routes are picked up by the configurator."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('blog', '/blog/{id:\d+}/{slug}')
    config.add_route('blog_action', '/blog/{action}')
    config.add_route('auth', '/sign/{action}')
