## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Products: Create Batch</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to Products", url('products'))}</li>
</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    $(function() {

        $('#batch_type').selectmenu();

        $('#make-batch').click(function() {
            $(this).button('disable').button('option', 'label', "Working, please wait...");
            $(this).parents('form:first').submit();
        });

    });
  </script>
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

% if supported_batches is not Undefined:

    <div class="form">

      ${h.form(request.current_route_url())}
      ${h.csrf_token(request)}

      <div class="field-wrapper">
        <label for="batch_type">Batch Type</label>
        <div class="field">
          ${h.select('batch_type', None, supported_batches)}
        </div>
      </div>

      <div class="buttons">
        <button type="button" id="make-batch">Create Batch</button>
        ${h.link_to("Cancel", url('products'), class_='button')}
      </div>

      ${h.end_form()}

    </div>

% else: ## legacy mode

    <div class="form">

      ${h.form(request.current_route_url())}
      ${h.csrf_token(request)}

      <div class="field-wrapper">
        <label for="provider">Batch Type</label>
        <div class="field">
          ${h.select('provider', None, providers)}
        </div>
      </div>

      <div class="buttons">
        ${h.submit('create', "Create Batch")}
        ${h.link_to("Cancel", url('products'), class_='button')}
      </div>

      ${h.end_form()}

    </div>

% endif
