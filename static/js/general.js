(function ($) {
    $(function () {
        $('table.table tr td').not('.options').click(function () {
            window.location.href = $(this).parent().data('url')
        });
    })
})(jQuery);