## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />

<%def name="context_menu()">
    % if request.has_perm('schedule.view'):
        <li>${h.link_to("View this Schedule", url('timesheet.goto.schedule'), class_='goto')}</li>
    % endif
</%def>

${self.timesheet()}
