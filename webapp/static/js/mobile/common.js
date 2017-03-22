function mobileMenu() {
    if ($('.side_menu_wrapper').css('display') == 'none'){
        $('.nav-guide-search-dropdown').hide('slow');
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            $('.mobile-header').animate({backgroundColor: "rgb(255, 255, 255)"});
        }
    }
    else {
        $('.nav-guide-search-dropdown').show('slow');
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            $('.mobile-header').animate({backgroundColor: "rgba(255, 255, 255, 0)"});
        }
    }
    $('.side_menu_wrapper').slideToggle();
}

function mobileSearch() {
    if ($('.search_side_menu_wrapper').css('display') == 'none'){
        $('.nav-menubar').hide('slow');
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            $('.mobile-header').animate({backgroundColor: "rgb(255, 255, 255)"});
        }
    }
    else {
        $('.nav-menubar').show('slow');
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            $('.mobile-header').animate({backgroundColor: "rgba(255, 255, 255, 0)"});
        }
    }
    $('.search_side_menu_wrapper').slideToggle();
}

function fixTripButton() {
    var container = $('.enroll-trip-button');
    var maxTop = $('footer').offset().top - container.outerHeight() - 20;
    var scrollVal = $(document).scrollTop() + $(window).height() - 80;

    if (scrollVal > maxTop) {
        container.css('top', maxTop);
    }

    else {
        container.stop().animate({top: scrollVal},'100');
    }
}

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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function(){
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    fixTripButton();
    $('.enroll-trip-button').fadeIn('slow');
    $(document).scroll(function() {
        fixTripButton();
    });

});
