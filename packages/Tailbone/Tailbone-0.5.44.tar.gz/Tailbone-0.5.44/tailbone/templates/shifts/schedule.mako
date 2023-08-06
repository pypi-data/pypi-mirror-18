## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />
<%namespace file="/shifts/lib.mako" import="timesheet_wrapper" />

<%def name="context_menu()">
  % if request.has_perm('schedule.edit'):
      <li>${h.link_to("Edit Schedule", url('schedule.edit'))}</li>
  % endif
  % if request.has_perm('schedule.print'):
      <li>${h.link_to("Print Schedule", url('schedule.print'), target='_blank')}</li>
  % endif
  % if request.has_perm('timesheet.view'):
      <li>${h.link_to("View this Time Sheet", url('schedule.goto.timesheet'), class_='goto')}</li>
  % endif
</%def>

${timesheet_wrapper(context_menu=context_menu, render_day=self.render_day)}
