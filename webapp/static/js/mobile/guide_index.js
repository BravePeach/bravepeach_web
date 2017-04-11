function fixGuideButton() {
    if($('.guide-button').offset().top + $('.guide-button').height()
                                           >= $('footer').offset().top - 70) {
        $('.guide-button').css('position', 'absolute');
        $('.guide-button').css('bottom', '323px');
    }
    if($(document).scrollTop() + window.innerHeight < $('footer').offset().top) {
        $('.guide-button').css('position', 'fixed'); // restore when you scroll up
        $('.guide-button').css('bottom', '50px');
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