(function ($) {

    $.fn.charsLeft = function (options) {

        var defaults = {
            source: 'input',
            dest: '.count'
        };

        var options = $.extend(defaults, options);

        var calculate = function (source, dest, maxlength) {
            var remaining = maxlength - source.val().length;
            dest.html(remaining);

            if (100 * remaining / maxlength < 20) {
                dest.addClass('charsleft-limit');
            } else {
                dest.removeClass('charsleft-limit');
            }
        };

        this.each(function (i, el) {
            var el = $(el);
            var maxlength = el.find('.maxlength').html();
            var dest = el.find(options.dest);
            var source = el.find(options.source);
            source.keyup(function () {
                calculate(source, dest, maxlength)
            });
            source.change(function () {
                calculate(source, dest, maxlength)
            });
        });
    };

    $(function () {

        $('.charsleft-input.charsleft-charfield').charsLeft({
            source: 'input',
            dest: ".count"
        });


        $('.charsleft-input.charsleft-textfield').charsLeft({
            source: 'textarea',
            dest: '.count'
        });

    });

})(django.jQuery);
