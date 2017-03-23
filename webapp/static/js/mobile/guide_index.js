function fixGuideButton() {
    var container = $('.guide-button');
    var maxTop = $('footer').offset().top - container.outerHeight() - 26.5;
    var scrollVal = $(document).scrollTop() + $(window).height() - 120;

    if (scrollVal > maxTop) {
        container.css('top', maxTop);
    }

    else {
        container.stop().animate({top: scrollVal},'100');
    }
}


$(function() {
    $(window).scroll(function () {
        if ($('header').offset().top < 100) {
            $('header').stop().animate({backgroundColor: "rgba(255, 255, 255, 0)"}, 'fast');
            $('.nav-bravepeach-logo').fadeOut();
        }
        else if ($('header').offset().top) {
            $('header').stop().animate({backgroundColor: "rgb(255, 255, 255)"}, 'fast');
            $('.nav-bravepeach-logo').fadeIn();
        }
    });

    fixGuideButton();
    $('.guide-button').fadeIn('slow');
    $(document).scroll(function() {
        $('.guide-button').fadeIn('slow');
        fixGuideButton();
    });

});