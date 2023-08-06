## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

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

<%def name="render_day(day)">
  % for shift in day['shifts']:
      <p class="shift">${render_shift(shift)}</p>
  % endfor
</%def>
