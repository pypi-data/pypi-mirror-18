## -*- coding: utf-8 -*-
<%inherit file="/newbatch/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    $(function() {

        $('#order-form').click(function() {
            % if vendor_cost_count > vendor_cost_threshold:
                if (! confirm("This vendor has ${'{:,d}'.format(vendor_cost_count)} cost records.\n\n" +
                              "It is not recommended to use Order Form mode for such a large catalog.\n\n" +
                              "Are you sure you wish to do it anyway?")) {
                    return;
                }
            % endif
            $(this).button('disable').button('option', 'label', "Working, please wait...");
            location.href = '${url('purchases.batch.order_form', uuid=batch.uuid)}';
        });

    });
  </script>
</%def>

<%def name="leading_buttons()">
  % if not batch.complete and not batch.executed and request.has_perm('purchases.batch.order_form'):
      <button type="button" id="order-form">View as Order Form</button>
  % endif
</%def>

${parent.body()}
