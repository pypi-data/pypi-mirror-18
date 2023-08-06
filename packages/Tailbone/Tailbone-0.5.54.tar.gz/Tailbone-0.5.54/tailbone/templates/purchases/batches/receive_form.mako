## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Receiving Form (${batch.vendor})</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/numeric.js'))}
  <script type="text/javascript">

    function assert_quantity() {
        if ($('#cases').val() && parseFloat($('#cases').val())) {
            return true;
        }
        if ($('#units').val() && parseFloat($('#units').val())) {
            return true;
        }
        alert("Please provide case and/or unit quantity");
        $('#cases').select().focus();
        return false;
    }

    function invalid_product(msg) {
        $('#received-product-info p').text(msg);
        $('#received-product-info img').hide();
        $('#received-product-info .rogue-item-warning').hide();
        $('#product-textbox').focus().select();
        $('.field-wrapper.cases input').prop('disabled', true);
        $('.field-wrapper.units input').prop('disabled', true);
        $('.buttons button').button('disable');
    }

    $(function() {

        $('#product-textbox').keydown(function(event) {

            if (key_allowed(event)) {
                return true;
            }
            if (key_modifies(event)) {
                $('#product').val('');
                $('#received-product-info p').html("please ENTER a scancode");
                $('#received-product-info img').hide();
                $('#received-product-info .rogue-item-warning').hide();
                $('.field-wrapper.cases input').prop('disabled', true);
                $('.field-wrapper.units input').prop('disabled', true);
                $('.buttons button').button('disable');
                return true;
            }
            if (event.which == 13) {
                var input = $(this);
                var data = {upc: input.val()};
                $.get('${url('purchases.batch.receiving_lookup', uuid=batch.uuid)}', data, function(data) {
                    if (data.error) {
                        alert(data.error);
                        if (data.redirect) {
                            $('#receiving-form').mask("Redirecting...");
                            location.href = data.redirect;
                        }
                    } else if (data.product) {
                        input.val(data.product.upc_pretty);
                        $('#product').val(data.product.uuid);
                        $('#received-product-info p').text(data.product.full_description);
                        $('#received-product-info img').attr('src', data.product.image_url).show();
                        $('#received-product-info .rogue-item-warning').hide();
                        if (! data.product.found_in_batch) {
                            $('#received-product-info .rogue-item-warning').show();
                        }
                        $('.field-wrapper.cases input').prop('disabled', false);
                        $('.field-wrapper.units input').prop('disabled', false);
                        $('.buttons button').button('enable');
                        $('#cases').focus().select();
                    } else {
                        invalid_product('product not found');
                    }
                });
            }
            return false;
        });

        $('#received').click(function() {
            if (! assert_quantity()) {
                return;
            }
            $(this).button('disable').button('option', 'label', "Working...");
            $('#mode').val('received');
            $('#receiving-form').submit();
        });

        $('#damaged').click(function() {
            if (! assert_quantity()) {
                return;
            }
            $(this).button('disable').button('option', 'label', "Working...");
            $('#mode').val('damaged');
            $('#receiving-form').submit();
        });

        $('#expiration input[type="date"]').datepicker();

        $('#expired').click(function() {
            if (! assert_quantity()) {
                return;
            }
            $(this).button('disable').button('option', 'label', "Working...");
            $('#mode').val('expired');
            $('#expiration').dialog({
                title: "Expiration Date",
                modal: true,
                buttons: [
                    {
                        text: "OK",
                        click: function() {
                            $('#expiration').dialog('close');
                            $('#receiving-form #expiration_date').val(
                                $('#expiration input[type="date"]').val());
                            $('#receiving-form').submit();
                        }
                    },
                    {
                        text: "Cancel",
                        click: function() {
                            $('#expired').button('option', 'label', "Expired").button('enable');
                            $('#expiration').dialog('close');
                        }
                    }
                ]
            });
        });

        $('#mispick').click(function() {
            if (! assert_quantity()) {
                return;
            }
            $(this).button('disable').button('option', 'label', "Working...");
            $('#ordered-product').val('');
            $('#ordered-product-textbox').val('');
            $('#ordered-product-info p').html("please ENTER a scancode");
            $('#ordered-product-info img').hide();
            $('#mispick-dialog').dialog({
                title: "Mispick - Ordered Product",
                modal: true,
                width: 400,
                buttons: [
                    {
                        text: "OK",
                        click: function() {
                            if ($('#ordered-product-info .warning').is(':visible')) {
                                alert("You must choose a product which was ordered.");
                                $('#ordered-product-textbox').select().focus();
                                return;
                            }
                            $('#mispick-dialog').dialog('close');
                            $('#mode').val('mispick');
                            $('#receiving-form').submit();
                        }
                    },
                    {
                        text: "Cancel",
                        click: function() {
                            $('#mispick').button('option', 'label', "Mispick").button('enable');
                            $('#mispick-dialog').dialog('close');
                        }
                    }
                ]
            });
        });

        $('#ordered-product-textbox').keydown(function(event) {

            if (key_allowed(event)) {
                return true;
            }
            if (key_modifies(event)) {
                $('#ordered_product').val('');
                $('#ordered-product-info p').html("please ENTER a scancode");
                $('#ordered-product-info img').hide();
                $('#ordered-product-info .warning').hide();
                return true;
            }
            if (event.which == 13) {
                var input = $(this);
                var data = {upc: input.val()};
                $.get('${url('purchases.batch.receiving_lookup', uuid=batch.uuid)}', data, function(data) {
                    if (data.error) {
                        alert(data.error);
                        if (data.redirect) {
                            $('#mispick-dialog').mask("Redirecting...");
                            location.href = data.redirect;
                        }
                    } else if (data.product) {
                        input.val(data.product.upc_pretty);
                        $('#ordered_product').val(data.product.uuid);
                        $('#ordered-product-info p').text(data.product.full_description);
                        $('#ordered-product-info img').attr('src', data.product.image_url).show();
                        if (data.product.found_in_batch) {
                            $('#ordered-product-info .warning').hide();
                        } else {
                            $('#ordered-product-info .warning').show();
                        }
                    } else {
                        $('#ordered-product-info p').text("product not found");
                        $('#ordered-product-info img').hide();
                        $('#ordered-product-info .warning').hide();
                    }
                });
            }
            return false;
        });

        $('#receiving-form').submit(function() {
            $(this).mask("Working...");
        });

        $('#product-textbox').focus();
        $('.field-wrapper.cases input').prop('disabled', true);
        $('.field-wrapper.units input').prop('disabled', true);
        $('.buttons button').button('disable');

    });
  </script>
  <style type="text/css">

    .product-info {
        margin-top: 0.5em;
        text-align: center;
    }

    .product-info p {
        margin-left: 0.5em;
    }

    .product-info .img-wrapper {
        height: 150px;
        margin: 0.5em 0;
    }

    .product-info .rogue-item-warning {
        background: #f66;
        display: none;
    }

    #mispick-dialog input[type="text"],
    #ordered-product-info {
        width: 320px;
    }

    #ordered-product-info .warning {
        background: #f66;
        display: none;
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
  ${form.begin(id='receiving-form')}
  ${h.hidden('mode')}
  ${h.hidden('expiration_date')}
  ${h.hidden('ordered_product')}

  <div class="field-wrapper">
    <label for="product-textbox">Product</label>
    <div class="field">
      ${h.hidden('product')}
      <div>${h.text('product-textbox', autocomplete='off')}</div>
      <div id="received-product-info" class="product-info">
        <p>please ENTER a scancode</p>
        <div class="img-wrapper"><img /></div>
        <div class="rogue-item-warning">warning: product not found on current purchase</div>
      </div>
    </div>
  </div>

  <div class="field-wrapper cases">
    <label for="cases">Cases</label>
    <div class="field">${h.text('cases', autocomplete='off')}</div>
  </div>

  <div class="field-wrapper units">
    <label for="units">Units</label>
    <div class="field">${h.text('units', autocomplete='off')}</div>
  </div>

  <div class="buttons">
    <button type="button" id="received">Received</button>
    <button type="button" id="damaged">Damaged</button>
    <button type="button" id="expired">Expired</button>
    <button type="button" id="mispick">Mispick</button>
  </div>

  ${form.end()}
</div>

<div id="expiration" style="display: none;">
  ${h.text('expiration-date', type='date')}
</div>

<div id="mispick-dialog" style="display: none;">
  <div>${h.text('ordered-product-textbox', autocomplete='off')}</div>
  <div id="ordered-product-info" class="product-info">
    <p>please ENTER a scancode</p>
    <div class="img-wrapper"><img /></div>
    <div class="warning">warning: product not found on current purchase</div>
  </div>
</div>
