# -*- coding: utf-8 -*-
"""
User views
"""

from __future__ import unicode_literals, absolute_import

from tailbone.views import users as base


class UsersView(base.UsersView):
    """
    Prevent edit/delete for 'chuck'
    """

    def editable_instance(self, user):
        return user.uuid != '28eeee92bcf411e6a7c23ca9f40bc550'

    def deletable_instance(self, user):
        return user.uuid != '28eeee92bcf411e6a7c23ca9f40bc550'


def includeme(config):
    UsersView.defaults(config)
