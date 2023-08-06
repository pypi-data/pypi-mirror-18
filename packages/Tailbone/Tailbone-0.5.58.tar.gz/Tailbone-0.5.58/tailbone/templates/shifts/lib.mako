## -*- coding: utf-8 -*-
<%namespace file="/autocomplete.mako" import="autocomplete" />

<%def name="timesheet_wrapper(edit_form=None, edit_tools=None, context_menu=None, render_day=None)">
    <div class="timesheet-wrapper">

      ${form.begin(id='filter-form')}
      ${form.csrf_token()}

      <table class="timesheet-header">
        <tbody>
          <tr>

            <td class="filters" rowspan="2">

              % if employee is not UNDEFINED:
                  <div class="field-wrapper employee">
                    <label>Employee</label>
                    <div class="field">
                      % if request.has_perm('{}.viewall'.format(permission_prefix)):
                          ${autocomplete('employee', url('employees.autocomplete'),
                                         field_value=employee.uuid if employee else None,
                                         field_display=unicode(employee or ''),
                                         selected='employee_selected')}
                      % else:
                          ${form.hidden('employee', value=employee.uuid)}
                          ${employee}
                      % endif
                    </div>
                  </div>
              % endif

              % if store_options is not UNDEFINED:
                  ${form.field_div('store', h.select('store', store.uuid if store else None, store_options))}
              % endif

              % if department_options is not UNDEFINED:
                  ${form.field_div('department', h.select('department', department.uuid if department else None,  department_options))}
              % endif

              <div class="field-wrapper week">
                <label>Week of</label>
                <div class="field">
                  ${week_of}
                </div>
              </div>

              % if edit_tools:
                  ${edit_tools()}
              % endif

            </td><!-- filters -->

            <td class="menu">
              <ul id="context-menu">
                % if context_menu:
                    ${context_menu()}
                % endif
              </ul>
            </td><!-- menu -->
          </tr>

          <tr>
            <td class="tools">
              <div class="grid-tools">
                <div class="week-picker">
                  <button type="button" class="nav" data-date="${prev_sunday.strftime('%m/%d/%Y')}">&laquo; Previous</button>
                  <button type="button" class="nav" data-date="${next_sunday.strftime('%m/%d/%Y')}">Next &raquo;</button>
                  <label>Jump to week:</label>
                  ${form.text('date', value=sunday.strftime('%m/%d/%Y'))}
                </div>
              </div><!-- grid-tools -->
            </td><!-- tools -->
          </tr>

        </tbody>
      </table><!-- timesheet-header -->

      ${form.end()}

      % if edit_form:
          ${edit_form()}
      % endif

      ${timesheet(render_day=render_day)}

      % if edit_form:
          ${h.end_form()}
      % endif

    </div><!-- timesheet-wrapper -->
</%def>

<%def name="timesheet(render_day=None)">
  <style type="text/css">
    .timesheet thead th {
         width: ${'{:0.2f}'.format(100.0 / 9)}%;
    }
  </style>

  <table class="timesheet">
    <thead>
      <tr>
        <th>Employee</th>
        % for day in weekdays:
            <th>${day.strftime('%A')}<br />${day.strftime('%b %d')}</th>
        % endfor
        <th>Total<br />Hours</th>
      </tr>
    </thead>
    <tbody>
      % for emp in sorted(employees, key=unicode):
          <tr data-employee-uuid="${emp.uuid}">
            <td class="employee">${emp}</td>
            % for day in emp.weekdays:
                <td class="day">
                  % if render_day:
                      ${render_day(day)}
                  % endif
                </td>
            % endfor
            <td class="total">${emp.hours_display}</td>
          </tr>
      % endfor
      % if employee is UNDEFINED:
          <tr class="total">
            <td class="employee">${len(employees)} employees</td>
            % for day in weekdays:
                <td></td>
            % endfor
            <td></td>
          </tr>
      % else:
          <tr>
            <td>&nbsp;</td>
            % for day in employee.weekdays:
                <td>${day['hours_display']}</td>
            % endfor
            <td>${employee.hours_display}</td>
          </tr>
      % endif
    </tbody>
  </table>
</%def>
