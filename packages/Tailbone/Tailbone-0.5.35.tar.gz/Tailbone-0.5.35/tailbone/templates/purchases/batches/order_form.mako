## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Purchase Order Form</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/numeric.js'))}
  <script type="text/javascript">
    $(function() {

        $('.order-form td.current-order input').keydown(function(event) {
            if (key_allowed(event) || key_modifies(event)) {
                return true;
            }
            if (event.which == 13) {
                var input = $(this);
                var row = input.parents('tr:first');
                var data = {
                    product_uuid: row.data('uuid'),
                    cases_ordered: input.val() || '0'
                };
                $.post('${url('purchases.batch.order_form_update', uuid=batch.uuid)}', data, function(data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        input.val(data.row_cases_ordered);
                        row.find('td:last').html(data.row_po_total);
                        $('.po-total .field').html(data.batch_po_total);
                    }
                });
            }
            return false;
        });

    });
  </script>
  <style type="text/css">

    .order-form th.department {
        border-top: 1px solid black;
        font-size: 1.2em;
        padding: 15px;
        text-align: left;
        text-transform: uppercase;
    }

    .order-form th.subdepartment {
        background-color: white;
        border-bottom: 1px solid black;
        border-top: 1px solid black;
        padding: 15px;
        text-align: left;
    }

    .order-form td {
        border-right: 1px solid #000000;
        border-top: 1px solid #000000;
    }

    .order-form td.upc,
    .order-form td.case-qty,
    .order-form td.code,
    .order-form td.preferred {
        text-align: center;
    }

    .order-form td.scratch_pad {
        width: 40px;
    }

    .order-form td.current-order input {
        text-align: center;
        width: 3em;
    }

    .order-form td.unit-cost,
    .order-form td.po-total {
        text-align: right;
    }

  </style>
</%def>


<%def name="context_menu_items()">
  <li>${h.link_to("Back to Purchase Batch", url('purchases.batch.view', uuid=batch.uuid))}</li>
</%def>


<ul id="context-menu">
  ${self.context_menu_items()}
</ul>


<div class="form-wrapper">

  <div class="field-wrapper">
    <label>Vendor</label>
    <div class="field">${vendor}</div>
  </div>

  <div class="field-wrapper">
    <label>Order Date</label>
    <div class="field">${batch.date_ordered}</div>
  </div>

  <div class="field-wrapper po-total">
    <label>PO Total</label>
    <div class="field">$${'{:0,.2f}'.format(batch.po_total or 0)}</div>
  </div>

</div><!-- form-wrapper -->


<div class="newgrid">
  <table class="order-form">
    % for department in sorted(departments.itervalues(), key=lambda d: d.name if d else ''):
        <thead>
          <tr>
            <th class="department" colspan="22">Department:&nbsp; ${department.number} ${department.name}</th>
          </tr>
          % for subdepartment in sorted(department._order_subdepartments.itervalues(), key=lambda s: s.name if s else ''):
              <tr>
                <th class="subdepartment" colspan="22">Subdepartment:&nbsp; ${subdepartment.number} ${subdepartment.name}</th>
              </tr>
              <tr>
                <th>UPC</th>
                <th>Brand</th>
                <th>Description</th>
                <th>Case</th>
                <th>Vend. Code</th>
                <th>Pref.</th>
                <th>Unit Cost</th>
                <th colspan="7">&nbsp;</th>
                <th>PO Total</th>
              </tr>
            </thead>
            <tbody>
              % for cost in subdepartment._order_costs:
                  <tr data-uuid="${cost.product_uuid}">
                    <td class="upc">${get_upc(cost.product)}</td>
                    <td class="brand">${cost.product.brand or ''}</td>
                    <td class="desc">${cost.product.description} ${cost.product.size or ''}</td>
                    <td class="case-qty">${cost.case_size} ${"LB" if cost.product.weighed else "EA"}</td>
                    <td class="code">${cost.code or ''}</td>
                    <td class="preferred">${'X' if cost.preference == 1 else ''}</td>
                    <td class="unit-cost">$${'{:0.2f}'.format(cost.unit_cost)}</td>
                    % for i in range(6):
                        <td class="scratch_pad">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                    % endfor
                    <td class="current-order">
                       ${h.text('cases_ordered_{}'.format(cost.uuid), value=int(cost._batchrow.cases_ordered) if cost._batchrow else None)}
                    </td>
                    <td class="po-total">${'${:0,.2f}'.format(cost._batchrow.po_total) if cost._batchrow else ''}</td>
                  </tr>
              % endfor
            </tbody>
        % endfor
    % endfor
  </table>
</div>
