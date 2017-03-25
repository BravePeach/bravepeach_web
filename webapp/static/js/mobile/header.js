// 모바일 헤더 에니메이션

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
    $('.side_menu_wrapper').toggle("slide", { direction: "right" })
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
    $('.search_side_menu_wrapper').toggle("slide", { direction: "left" })
}

$(function () {
    $('.find-guide-form, .find-guide-form2').click(function () {
        mobileSearch();
    });
});