function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function fixTripButton() {
    var container = $('.enroll-trip-button');
    var maxTop = $('footer').offset().top - container.outerHeight() - 26.5;
    var scrollVal = $(document).scrollTop() + $(window).height() - 120;

    container.css('top', scrollVal);
    if (container.offset().top > maxTop) {
        container.css('top', maxTop);
    }
}

$(function(){
    fixTripButton();
    $('.enroll-trip-button').fadeIn('slow');
    $(document).scroll(function(){
        fixTripButton();
    });
});
