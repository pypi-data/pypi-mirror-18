## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />

<%def name="context_menu()">
  % if request.has_perm('schedule.edit'):
      <li>${h.link_to("Edit Schedule", url('schedule.edit'))}</li>
  % endif
  % if request.has_perm('timesheet.view'):
      <li>${h.link_to("View this Time Sheet", url('schedule.goto.timesheet'), class_='goto')}</li>
  % endif
</%def>

${self.timesheet()}
