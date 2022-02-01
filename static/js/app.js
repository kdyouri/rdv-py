$(document).on('mouseenter', '[data-bs-toggle="tooltip"]', function(){
    var tooltip = $(this).data('tooltip');

    if (!tooltip) {
        tooltip = new bootstrap.Tooltip(this, {
            container: 'body'
        });
        $(this).data('tooltip', tooltip);
    }
    tooltip.show();
});

$(document).on('content.loaded', '.xcrud-modal', function(){
    var $modal = $(this);

    $(this).find('.select2').each(function(){
        $(this).select2({
            theme: "bootstrap-5",
            // width: $(this).data("width") ? $(this).data("width") : $(this).hasClass("w-100") ? "100%" : "style",
            // placeholder: $(this).data("placeholder"),
            // allowClear: Boolean($(this).data("allow-clear")),
            // closeOnSelect: !$(this).attr("multiple"),
            // containerCssClass: "select2--small",
            // selectionCssClass: "select2--small",
            // dropdownCssClass: "select2--small",
            dropdownParent: $modal
        });
    } );
});

bootbox.setLocale('fr');