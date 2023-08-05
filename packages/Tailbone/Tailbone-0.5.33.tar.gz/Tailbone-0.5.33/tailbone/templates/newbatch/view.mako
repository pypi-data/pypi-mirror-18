## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.batch.js'))}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options else 'false'};

    $(function() {
        $('#refresh-data').click(function() {
            $(this)
                .button('option', 'disabled', true)
                .button('option', 'label', "Working, please wait...");
            location.href = '${url('{}.refresh'.format(route_prefix), uuid=batch.uuid)}';
        });
    });

  </script>
  <style type="text/css">

    .newgrid-wrapper {
        margin-top: 10px;
    }
    
  </style>
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if master.rows_downloadable and request.has_perm('{}.csv'.format(permission_prefix)):
      <li>${h.link_to("Download row data as CSV", url('{}.csv'.format(route_prefix), uuid=batch.uuid))}</li>
  % endif
</%def>

<%def name="buttons()">
## TODO: the refreshable thing still seems confusing...
    <div class="buttons">
      % if master.refreshable:
          % if form.readonly:
              % if not batch.executed:
                  <button type="button" id="refresh-data">Refresh Data</button>
              % endif
          % elif batch.refreshable:
              ${h.submit('save-refresh', "Save & Refresh Data")}
          % endif
      % endif
      % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
          <button type="button" id="execute-batch"${'' if execute_enabled else ' disabled="disabled"'}>${execute_title}</button>
      % endif
    </div>
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render(form_id='batch-form', buttons=capture(buttons))|n}
</div><!-- form-wrapper -->

${rows_grid|n}

<div id="execution-options-dialog" style="display: none;">

  ${h.form(url('{}.execute'.format(route_prefix), uuid=batch.uuid), name='batch-execution')}
  % if master.has_execution_options:
      ${rendered_execution_options|n}
  % endif
  ${h.end_form()}

</div>
