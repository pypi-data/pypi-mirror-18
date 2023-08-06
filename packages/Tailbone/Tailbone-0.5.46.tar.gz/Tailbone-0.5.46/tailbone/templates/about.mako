## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">About ${project_title}</%def>

<h2>${project_title} ${project_version}</h2>

% for name, version in packages.iteritems():
    <h3>${name} ${version}</h3>
% endfor
