# -*- coding: utf-8 -*-
"""
Common views
"""

from __future__ import unicode_literals, absolute_import

from tailbone.views import common as base

import rattail_demo


class CommonView(base.CommonView):

    project_title = "Rattail Demo"
    project_version = rattail_demo.__version__


def includeme(config):
    CommonView.defaults(config)
