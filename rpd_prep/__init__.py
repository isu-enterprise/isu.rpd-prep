
from pyramid.events import subscriber, BeforeRender
from pyramid.interfaces import IRendererFactory
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
