## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />
<%namespace file="/shifts/lib.mako" import="timesheet_wrapper" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">

    var weekdays = [
        % for i, day in enumerate(weekdays, 1):
            '${day.strftime('%a %d %b %Y')}'${',' if i < len(weekdays) else ''}
        % endfor
    ];

    var editing_day = null;
    var new_shift_id = 1;

    function add_shift(focus, uuid, start_time, end_time) {
        var shift = $('#snippets .shift').clone();
        if (! uuid) {
            uuid = 'new-' + (new_shift_id++).toString();
        }
        shift.attr('data-uuid', uuid);
        shift.children('input').each(function() {
            var name = $(this).attr('name') + '-' + uuid;
            $(this).attr('name', name);
            $(this).attr('id', name);
        });
        shift.children('input[name|="edit_start_time"]').val(start_time || '');
        shift.children('input[name|="edit_end_time"]').val(end_time || '');
        $('#day-editor .shifts').append(shift);
        shift.children('input').timepicker({showPeriod: true});
        if (focus) {
            shift.children('input:first').focus();
        }
    }

    function calc_minutes(start_time, end_time) {
        var start = parseTime(start_time);
        start = new Date(2000, 0, 1, start.hh, start.mm);
        var end = parseTime(end_time);
        end = new Date(2000, 0, 1, end.hh, end.mm);
        return Math.floor((end - start) / 1000 / 60);
    }

    function format_minutes(minutes) {
        var hours = Math.floor(minutes / 60);
        if (hours) {
            minutes -= hours * 60;
        }
        return hours.toString() + ':' + (minutes < 10 ? '0' : '') + minutes.toString();
    }

    // stolen from http://stackoverflow.com/a/1788084
    function parseTime(s) {
        var part = s.match(/(\d+):(\d+)(?: )?(am|pm)?/i);
        var hh = parseInt(part[1], 10);
        var mm = parseInt(part[2], 10);
        var ap = part[3] ? part[3].toUpperCase() : null;
        if (ap == 'AM') {
            if (hh == 12) {
                hh = 0;
            }
        } else if (ap == 'PM') {
            if (hh != 12) {
                hh += 12;
            }
        }
        return { hh: hh, mm: mm };
    }

    function time_input(shift, type) {
        var input = shift.children('input[name|="' + type + '_time"]');
        if (! input.length) {
            input = $('<input type="hidden" name="' + type + '_time-' + shift.data('uuid') + '" />');
            shift.append(input);
        }
        return input;
    }

    function update_row_hours(row) {
        var minutes = 0;
        row.find('.day .shift:not(.deleted)').each(function() {
            var time_range = $.trim($(this).children('span').text()).split(' - ');
            minutes += calc_minutes(time_range[0], time_range[1]);
        });
        row.children('.total').text(minutes ? format_minutes(minutes) : '0');
    }

    $(function() {

        $('.timesheet').on('click', '.day', function() {
            editing_day = $(this);
            var editor = $('#day-editor');
            var employee = editing_day.siblings('.employee').text();
            var date = weekdays[editing_day.get(0).cellIndex - 1];
            var shifts = editor.children('.shifts');
            shifts.empty();
            editing_day.children('.shift:not(.deleted)').each(function() {
                var uuid = $(this).data('uuid');
                var time_range = $.trim($(this).children('span').text()).split(' - ');
                add_shift(false, uuid, time_range[0], time_range[1]);
            });
            if (! shifts.children('.shift').length) {
                add_shift();
            }
            editor.dialog({
                modal: true,
                title: employee + ' - ' + date,
                position: {my: 'center', at: 'center', of: editing_day},
                width: 'auto',
                autoResize: true,
                buttons: [
                    {
                        text: "Update",
                        click: function() {

                            // TODO: need to validate times here...

                            // create / update shifts in schedule table, as needed
                            editor.find('.shifts .shift').each(function() {
                                var uuid = $(this).data('uuid');
                                var start_time = $(this).children('input[name|="edit_start_time"]').val();
                                var end_time = $(this).children('input[name|="edit_end_time"]').val();
                                var shift = editing_day.children('.shift[data-uuid="' + uuid + '"]');
                                if (! shift.length) {
                                    shift = $('<p class="shift" data-uuid="' + uuid + '"><span></span></p>');
                                    shift.append($('<input type="hidden" name="employee_uuid-' + uuid + '" value="'
                                                   + editing_day.parents('tr:first').data('employee-uuid') + '" />'));
                                    ## TODO: how to handle editing schedule w/ no store selected..?
                                    % if store:
                                        shift.append($('<input type="hidden" name="store_uuid-' + uuid + '" value="${store.uuid}" />'));
                                    % endif
                                    editing_day.append(shift);
                                }
                                shift.children('span').text(start_time + ' - ' + end_time);
                                time_input(shift, 'start').val(date + ' ' + start_time);
                                time_input(shift, 'end').val(date + ' ' + end_time);
                            });

                            // remove shifts from schedule table, as needed
                            editing_day.children('.shift').each(function() {
                                var uuid = $(this).data('uuid');
                                if (! editor.find('.shifts .shift[data-uuid="' + uuid + '"]').length) {
                                    if (uuid.match(/^new-/)) {
                                        $(this).remove();
                                    } else {
                                        $(this).addClass('deleted');
                                        $(this).append($('<input type="hidden" name="delete-' + uuid + '" value="delete" />'));
                                    }
                                }
                            });

                            // mark day as modified, close dialog
                            editing_day.addClass('modified');
                            $('.save-changes').button('enable');
                            $('.undo-changes').button('enable');
                            update_row_hours(editing_day.parents('tr:first'));
                            editor.dialog('close');
                            data_modified = true;
                            okay_to_leave = false;
                        }
                    },
                    {
                        text: "Cancel",
                        click: function() {
                            editor.dialog('close');
                        }
                    }
                ]
            });
        });

        $('#day-editor #add-shift').click(function() {
            add_shift(true);
        });

        $('#day-editor').on('click', '.shifts button', function() {
            $(this).parents('.shift:first').remove();
        });

        $('.save-changes').click(function() {
            $(this).button('disable').button('option', 'label', "Saving Changes...");
            okay_to_leave = true;
            $('#schedule-form').submit();
        });

        $('.undo-changes').click(function() {
            $(this).button('disable').button('option', 'label', "Refreshing...");
            okay_to_leave = true;
            location.href = '${url('schedule.edit')}';
        });

        $('.clear-schedule').click(function() {
            if (confirm("This will remove all shifts from the schedule you're " +
                        "currently viewing.\n\nAre you sure you wish to do this?")) {
                $(this).button('disable').button('option', 'label', "Clearing...");
                okay_to_leave = true;
                $('#clear-schedule-form').submit();
            }
        });

        $('#copy-week').datepicker({
            dateFormat: 'mm/dd/yy'
        });

        $('.copy-schedule').click(function() {
            $('#copy-details').dialog({
                modal: true,
                title: "Copy from Another Week",
                width: '500px',
                buttons: [
                    {
                        text: "Copy Schedule",
                        click: function(event) {
                            if (! $('#copy-week').val()) {
                                alert("You must specify the week from which to copy shift data.");
                                $('#copy-week').focus();
                                return;
                            }
                            $(event.target).button('disable').button('option', 'label', "Copying Schedule...");
                            $('#copy-schedule-form').submit();
                        }
                    },
                    {
                        text: "Cancel",
                        click: function() {
                            $('#copy-details').dialog('close');
                        }
                    }
                ]
            });
        });

    });
  </script>
  <style type="text/css">
    .timesheet .day {
        cursor: pointer;
        height: 5em;
    }
    .timesheet tr .day.modified {
        background-color: #fcc;
    }
    .timesheet tr:nth-child(odd) .day.modified {
        background-color: #ebb;
    }
    .timesheet .day .shift.deleted {
        display: none;
    }
    #day-editor .shift {
        margin-bottom: 1em;
        white-space: nowrap;
    }
    #day-editor .shift input {
        width: 6em;
    }
    #day-editor .shift button {
        margin-left: 0.5em;
    }
    #snippets {
        display: none;
    }
  </style>
</%def>

<%def name="context_menu()">
  % if request.has_perm('schedule.viewall'):
      <li>${h.link_to("View Schedule", url('schedule'))}</li>
  % endif
  % if request.has_perm('schedule.print'):
      <li>${h.link_to("Print Schedule", url('schedule.print'), target='_blank')}</li>
  % endif
</%def>

<%def name="render_day(day)">
  % for shift in day['shifts']:
      <p class="shift" data-uuid="${shift.uuid}">
        ${render_shift(shift)}
      </p>
  % endfor
</%def>

<%def name="edit_form()">
  ${h.form(url('schedule.edit'), id='schedule-form')}
  ${h.csrf_token(request)}
</%def>

<%def name="edit_tools()">
  <div class="buttons">
    <button type="button" class="save-changes" disabled="disabled">Save Changes</button>
    <button type="button" class="undo-changes" disabled="disabled">Undo Changes</button>
    <button type="button" class="clear-schedule">Clear Schedule</button>
    <button type="button" class="copy-schedule">Copy Schedule From...</button>
  </div>
</%def>

${timesheet_wrapper(edit_form=edit_form, edit_tools=edit_tools, context_menu=context_menu, render_day=render_day)}

${edit_tools()}

${h.form(url('schedule.edit'), id="clear-schedule-form")}
${h.csrf_token(request)}
${h.hidden('clear-schedule', value='clear')}
${h.end_form()}

<div id="day-editor" style="display: none;">
  <div class="shifts"></div>
  <button type="button" id="add-shift">Add Shift</button>
</div>

<div id="copy-details" style="display: none;">
  <p>
    This tool will replace the currently visible schedule, with one from
    another week.
  </p>
  <p>
    <strong>NOTE:</strong>&nbsp; If you do this, all shifts in the current
    schedule will be <em>removed</em>,
    and then new shifts will be created based on the week you specify.
  </p>
  ${h.form(url('schedule.edit'), id='copy-schedule-form')}
  ${h.csrf_token(request)}
  <label for="copy-week">Copy from week:</label>
  ${h.text('copy-week')}
  ${h.end_form()}
</div>

<div id="snippets">
  <div class="shift" data-uuid="">
    ${h.text('edit_start_time')} thru ${h.text('edit_end_time')}
    <button type="button"><span class="ui-icon ui-icon-trash"></span></button>
  </div>
</div>
