# -*- coding: utf-8 -*-
"""
Person views
"""

from __future__ import unicode_literals, absolute_import

from tailbone.views import people as base


class PeopleView(base.PeopleView):
    """
    Prevent edit/delete for Chuck Norris
    """

    def editable_instance(self, person):
        return person.uuid != '30d1fe06bcf411e6a7c23ca9f40bc550'

    def deletable_instance(self, person):
        return person.uuid != '30d1fe06bcf411e6a7c23ca9f40bc550'


def includeme(config):
    PeopleView.defaults(config)
