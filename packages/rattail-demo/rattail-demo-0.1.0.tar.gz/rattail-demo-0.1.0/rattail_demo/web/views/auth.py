# -*- coding: utf-8 -*-
"""
Auth views
"""

from __future__ import unicode_literals, absolute_import

from pyramid import httpexceptions

from tailbone.views import auth as base


def change_password(request):
    # prevent password change for 'chuck'
    if request.user and request.user.username == 'chuck':
        request.session.flash("Cannot change password for 'chuck' in Rattail Demo")
        return httpexceptions.HTTPFound(location=request.get_referrer())
    return base.change_password(request)


def includeme(config):
    # TODO: this is way too much duplication, surely..
    base.add_routes(config)

    config.add_forbidden_view(base.forbidden)

    config.add_view(base.login, route_name='login',
                    renderer='/login.mako')

    config.add_view(base.logout, route_name='logout')

    config.add_view(base.become_root, route_name='become_root')
    config.add_view(base.stop_root, route_name='stop_root')

    config.add_view(change_password, route_name='change_password',
                    renderer='/change_password.mako')
