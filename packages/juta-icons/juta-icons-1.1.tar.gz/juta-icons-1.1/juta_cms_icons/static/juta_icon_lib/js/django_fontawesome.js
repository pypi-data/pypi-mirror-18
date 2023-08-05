if (!$) {
    var $ = jQuery = django.jQuery;
}


$(function() {

    var prefix = $('select.juta-icon-select').data('juta-icon-prefix');

    function format(state) {
        if (!state.id) { return state.text; }
        var icon = $(state.element).data('icon');
        return '<span class="juta-portfolio-icon-' + state.text + '"></span><span class="mls">' + state.text + '</span>';

    }



    $('.juta-icon-select').select2({
        width:'element',
        formatResult:format,
        formatSelection:format,
        escapeMarkup: function(m) {return m;}
    });
});