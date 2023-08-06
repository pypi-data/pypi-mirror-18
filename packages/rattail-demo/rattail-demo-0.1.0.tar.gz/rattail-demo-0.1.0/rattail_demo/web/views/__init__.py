# -*- coding: utf-8 -*-
"""
Web views
"""

from __future__ import unicode_literals, absolute_import

from tailbone import views as base


def bogus_error(request):
    """
    A special view which simply raises an error, for the sake of testing
    uncaught exception handling.
    """
    raise Exception("Congratulations, you have triggered a bogus error.")


def includeme(config):

    # TODO: merge these views into core/common
    config.add_route('home', '/')
    config.add_view(base.home, route_name='home', renderer='/home.mako')
    config.add_route('bogus_error', '/bogus-error')
    config.add_view(bogus_error, route_name='bogus_error',
                    permission='admin')

    # core views
    config.include('rattail_demo.web.views.common')
    config.include('rattail_demo.web.views.auth')

    # main table views
    config.include('tailbone.views.brands')
    config.include('tailbone.views.customers')
    config.include('tailbone.views.departments')
    config.include('tailbone.views.employees')
    config.include('tailbone.views.families')
    config.include('rattail_demo.web.views.people')
    config.include('tailbone.views.products')
    config.include('tailbone.views.reportcodes')
    config.include('tailbone.views.roles')
    config.include('tailbone.views.settings')
    config.include('tailbone.views.stores')
    config.include('tailbone.views.subdepartments')
    config.include('rattail_demo.web.views.users')
    config.include('tailbone.views.vendors')

    # batch views
    config.include('tailbone.views.handheld')
    config.include('tailbone.views.inventory')
