/* The following line defines global variables defined elsewhere. */
/*globals $, jQuery*/

jQuery(function ($) {
    $('#portal-globalnav .noClick').click(function (e) {
        e.preventDefault();
    });

    $('ul.nav li.dropdown').hover(function() {
        $(this).closest('.dropdown-menu').stop(true, true).show();
        $(this).addClass('open');
    }, function() {
        $(this).closest('.dropdown-menu').stop(true, true).hide();
        $(this).removeClass('open');
    });
});

