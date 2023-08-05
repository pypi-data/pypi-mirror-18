## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<%namespace file="/autocomplete.mako" import="autocomplete" />

<%def name="title()">${page_title}</%def>

<%def name="head_tags()">
    ${parent.head_tags()}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/timesheet.css'))}
    <script type="text/javascript">

      var data_modified = false;
      var okay_to_leave = true;
      var previous_selections = {};

      window.onbeforeunload = function() {
          if (! okay_to_leave) {
              return "If you leave this page, you will lose all unsaved changes!";
          }
      }

      function employee_selected(uuid, name) {
          $('#filter-form').submit();
      }

      function confirm_leave() {
          if (data_modified) {
              if (confirm("If you navigate away from this page now, you will lose " +
                          "unsaved changes.\n\nAre you sure you wish to do this?")) {
                  okay_to_leave = true;
                  return true;
              }
              return false;
          }
          return true;
      }

      $(function() {

          $('#filter-form').submit(function() {
              $('.timesheet-header').mask("Fetching data");
          });

          $('.timesheet-header select').each(function() {
              previous_selections[$(this).attr('name')] = $(this).val();
          });

          $('.timesheet-header select').selectmenu({
              change: function(event, ui) {
                  if (confirm_leave()) {
                      $('#filter-form').submit();
                  } else {
                      var select = ui.item.element.parents('select');
                      select.val(previous_selections[select.attr('name')]);
                      select.selectmenu('refresh');
                  }
              }
          });

          $('.timesheet-header a.goto').click(function() {
              $('.timesheet-header').mask("Fetching data");
          });

          $('.week-picker button.nav').click(function() {
              if (confirm_leave()) {
                  $('.week-picker #date').val($(this).data('date'));
                  $('#filter-form').submit();
              }
          });

          $('.week-picker #date').datepicker({
              dateFormat: 'mm/dd/yy',
              changeYear: true,
              changeMonth: true,
              showButtonPanel: true,
              onSelect: function(dateText, inst) {
                  $('#filter-form').submit();
              }
          });

      });

    </script>
</%def>

<%def name="context_menu()"></%def>

<%def name="timesheet(edit_form=None, edit_tools=None)">
    <style type="text/css">
      .timesheet thead th {
           width: ${'{:0.2f}'.format(100.0 / 9)}%;
      }
    </style>

    <div class="timesheet-wrapper">

      ${form.begin(id='filter-form')}

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
                ${self.context_menu()}
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
                      ${self.render_day(day)}
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

      % if edit_form:
          ${h.end_form()}
      % endif

    </div><!-- timesheet-wrapper -->
</%def>

<%def name="render_day(day)">
  % for shift in day['shifts']:
      <p class="shift">${render_shift(shift)}</p>
  % endfor
</%def>
