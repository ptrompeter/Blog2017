"""Base init for Blog2017 WSGI app."""
import os
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    authentication_policy = AuthTktAuthenticationPolicy(os.environ.get('AUTH_STRING'))
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
