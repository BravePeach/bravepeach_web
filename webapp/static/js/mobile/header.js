function mobileMenu() {
    if ($('.side_menu_wrapper').css('display') == 'none'){
        $('.nav-menubar').attr("src", "/static/image/icon/cancel.png");
        $('html').addClass('not-scroll');
        $('.nav-guide-search-dropdown').hide();
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            // $('.mobile-header').animate({backgroundColor: "rgb(255, 255, 255)"});
            $('.mobile-header').css({backgroundColor: "rgb(255, 255, 255)"});
        }
        $('.side_menu_wrapper').show();
    }
    else {
        $('.nav-menubar').attr("src", "/static/image/icon/menu_bar.png");
        $('html').removeClass('not-scroll');
        $('.nav-guide-search-dropdown').show();
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            // $('.mobile-header').animate({backgroundColor: "rgba(255, 255, 255, 0)"});
            $('.mobile-header').css({backgroundColor: "rgba(255, 255, 255, 0)"});
        }
        $('.side_menu_wrapper').hide();
    }
    // $('.side_menu_wrapper').toggle("slide", { direction: "right" })
}

function mobileSearch() {
    if ($('.search_side_menu_wrapper').css('display') == 'none'){
        $('.nav-guide-search-dropdown').attr("src", "/static/image/icon/cancel.png");
        $('html').addClass('not-scroll');
        $('.nav-menubar').hide();
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            // $('.mobile-header').animate({backgroundColor: "rgb(255, 255, 255)"});
            $('.mobile-header').css({backgroundColor: "rgb(255, 255, 255)"});
        }
        $('.search_side_menu_wrapper').show()
    }
    else {
        $('.nav-guide-search-dropdown').attr("src", "/static/image/icon/Search_Icon.png");
        $('html').removeClass('not-scroll');
        $('.nav-menubar').show();
        if($('.nav-bravepeach-logo').css('display') == 'none') {
            // $('.mobile-header').animate({backgroundColor: "rgba(255, 255, 255, 0)"});
            $('.mobile-header').css({backgroundColor: "rgba(255, 255, 255, 0)"});
        }
        $('.search_side_menu_wrapper').hide()
    }
    // $('.search_side_menu_wrapper').toggle("slide", { direction: "left" })
}

$(function () {
    $('.find-guide-form, .find-guide-form2').click(function () {
        mobileSearch();
    });

    $(".folding").click(function(){
        var target = $(this);
        var target_class = target.attr("class").split(" ")[0];
        if(target.hasClass("folding")) {
            target.removeClass("folding");
            $(".second."+target_class).removeClass("folded");
            target.find("img").addClass("turn");
        } else {
            target.addClass("folding");
            $(".second."+target_class).addClass("folded");
            target.find("img").removeClass("turn");
        }
    });
});