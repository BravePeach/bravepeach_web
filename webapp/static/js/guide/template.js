$(function () {
    $('span.accom, span.guide, span.product').click(function () {
        $(this).siblings().removeClass('clicked');
        $(this).addClass('clicked');
        $('.wrapper').children().addClass('display-none');
        var clickedClass = $(this).attr('class').split(' ')[0];
        $('div.' + clickedClass).removeClass('display-none');
    });
});