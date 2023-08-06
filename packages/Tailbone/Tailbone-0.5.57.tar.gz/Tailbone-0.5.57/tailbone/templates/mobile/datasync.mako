## -*- coding: utf-8 -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">DataSync</%def>

${h.form(url('datasync.restart'))}
${h.submit('restart', "Restart DataSync Daemon", id='datasync-restart')}
${h.end_form()}
