# -*- coding: utf-8 -*-
"""
Pyramid web application
"""

from __future__ import unicode_literals, absolute_import

from tailbone import app


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # set some defaults for PostgreSQL
    app.provide_postgresql_settings(settings)

    # prefer demo templates over tailbone; use 'better' theme
    settings.setdefault('mako.directories', ['rattail_demo.web:templates',
                                             'tailbone:templates/themes/better',
                                             'tailbone:templates',])

    # make config objects
    rattail_config = app.make_rattail_config(settings)
    pyramid_config = app.make_pyramid_config(settings)

    # bring in rest of rattail-demo etc.
    pyramid_config.include('tailbone.static')
    pyramid_config.include('tailbone.subscribers')
    pyramid_config.include('rattail_demo.web.views')

    # configure PostgreSQL some more
    app.configure_postgresql(pyramid_config)

    return pyramid_config.make_wsgi_app()
