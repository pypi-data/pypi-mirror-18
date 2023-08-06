
/************************************************************
 *
 * tailbone.mobile.js
 *
 * Global logic for mobile app
 *
 ************************************************************/


$(function() {

    // must init header/footer toolbars since ours are "external"
    $('[data-role="header"], [data-role="footer"]').toolbar({theme: 'a'});
});


$(document).on('pagecontainerchange', function(event, ui) {

    // in some cases (i.e. when no user is logged in) we may want the (external)
    // header toolbar button to change between pages.  here's how we do that.
    // note however that we do this *always* even when not technically needed
    var link = $('[data-role="header"] a');
    var newlink = ui.toPage.find('.replacement-header a');
    link.text(newlink.text());
    link.attr('href', newlink.attr('href'));
    link.removeClass('ui-icon-home ui-icon-user');
    link.addClass(newlink.attr('class'));
});


$(document).on('pageshow', function() {

    // on login page, auto-focus username
    el = $('#username');
    if (el.is(':visible')) {
        el.focus();
    }

    // TODO: seems like this should be better somehow...
    // remove all flash messages after 2.5 seconds
    window.setTimeout(function() { $('.flash, .error').remove(); }, 2500);

});


$(document).on('click', '#datasync-restart', function() {

    // disable datasync restart button when clicked
    $(this).button('disable');
});
