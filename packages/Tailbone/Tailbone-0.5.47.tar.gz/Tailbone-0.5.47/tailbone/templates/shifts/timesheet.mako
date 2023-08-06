## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />
<%namespace file="/shifts/lib.mako" import="timesheet_wrapper" />

<%def name="context_menu()">
    % if request.has_perm('schedule.view'):
        <li>${h.link_to("View this Schedule", url('timesheet.goto.schedule'), class_='goto')}</li>
    % endif
</%def>

${timesheet_wrapper(context_menu=context_menu, render_day=self.render_day)}
