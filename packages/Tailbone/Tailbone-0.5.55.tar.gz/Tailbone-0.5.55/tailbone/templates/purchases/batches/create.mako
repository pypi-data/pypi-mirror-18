## -*- coding: utf-8 -*-
<%inherit file="/newbatch/create.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">

    function show_mode(mode) {
        if (mode == ${enum.PURCHASE_BATCH_MODE_NEW}) {
            $('.field-wrapper.store_uuid').show();
            $('.field-wrapper.purchase_uuid').hide();
            $('.field-wrapper.department_uuid').show();
            $('.field-wrapper.buyer_uuid').show();
            $('.field-wrapper.date_ordered').show();
            $('.field-wrapper.date_received').hide();
            $('.field-wrapper.invoice_date').hide();
            $('.field-wrapper.invoice_number').hide();
        } else if (mode == ${enum.PURCHASE_BATCH_MODE_RECEIVING}) {
            $('.field-wrapper.store_uuid').hide();
            $('.field-wrapper.purchase_uuid').show();
            $('.field-wrapper.department_uuid').hide();
            $('.field-wrapper.buyer_uuid').hide();
            $('.field-wrapper.date_ordered').hide();
            $('.field-wrapper.date_received').show();
            $('.field-wrapper.invoice_date').show();
            $('.field-wrapper.invoice_number').show();
        } else if (mode == ${enum.PURCHASE_BATCH_MODE_COSTING}) {
            $('.field-wrapper.store_uuid').hide();
            $('.field-wrapper.purchase_uuid').show();
            $('.field-wrapper.department_uuid').hide();
            $('.field-wrapper.buyer_uuid').hide();
            $('.field-wrapper.date_ordered').hide();
            $('.field-wrapper.date_received').hide();
            $('.field-wrapper.invoice_date').show();
            $('.field-wrapper.invoice_number').show();
        }
    }

    function vendor_selected(uuid, name) {
        var mode = $('.mode select').val();
        if (mode == ${enum.PURCHASE_BATCH_MODE_RECEIVING} || mode == ${enum.PURCHASE_BATCH_MODE_COSTING}) {
            var purchases = $('.purchase_uuid select');
            purchases.empty();

            var data = {'vendor_uuid': uuid, 'mode': mode};
            $.get('${url('purchases.batch.eligible_purchases')}', data, function(data) {
                if (data.error) {
                    alert(data.error);
                } else {
                    $.each(data.purchases, function(i, purchase) {
                        purchases.append($('<option value="' + purchase.uuid + '">' + purchase.display + '</option>'));
                    });
                }
            });

            // TODO: apparently refresh doesn't work right?
            // http://stackoverflow.com/a/10280078
            // purchases.selectmenu('refresh');
            purchases.selectmenu('destroy').selectmenu();
        }
    }

    function vendor_cleared() {
        var purchases = $('.purchase_uuid select');
        purchases.empty();

        // TODO: apparently refresh doesn't work right?
        // http://stackoverflow.com/a/10280078
        // purchases.selectmenu('refresh');
        purchases.selectmenu('destroy').selectmenu();
    }

    $(function() {

        $('.field-wrapper.mode select').selectmenu({
            change: function(event, ui) {
                show_mode(ui.item.value);
            }
        });

        $('.field-wrapper.purchase_uuid select').selectmenu();
        $('.field-wrapper.department_uuid select').selectmenu();

        show_mode(${form.fieldset.model.mode or enum.PURCHASE_BATCH_MODE_NEW});

    });

  </script>
</%def>

${parent.body()}
