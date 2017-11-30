"""Base init for Blog2017 WSGI app."""
import os
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator
import sys


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    if not settings.get('sqlalchemy.url'):
        try:
            settings['sqlalchemy.url'] = os.environ['BLOG2017_DB']
        except KeyError:
            print('Required BLOG2017_DB not set in global os environ.')
            sys.exit()

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
