## -*- coding: utf-8 -*-
<%inherit file="tailbone:templates/themes/better/base.mako" />

<%def name="global_title()">${"[STAGE] " if not request.rattail_config.production() else ''}Rattail Demo</%def>

<%def name="favicon()">
  <link rel="icon" type="image/x-icon" href="${request.static_url('tailbone:static/img/rattail.ico')}" />
</%def>

<%def name="header_logo()">
  ${h.image(request.static_url('tailbone:static/img/rattail.ico'), "Header Logo", height='49')}
</%def>

${parent.body()}
