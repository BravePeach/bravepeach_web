traveler_list = [0, 0, 0, 0, 0, 0];
city_list = [];

function submit_enroll_form(){
    $("#id_city").val(city_list.join());
    $("#enroll-form").submit();
}

$(function() {
    $( window ).scroll(function() {
        if($('header').offset().top < 204) {
            $('header').stop().animate({backgroundColor: "rgba(255, 255, 255, 0)"}, 'fast');
            $('.nav-bravepeach-logo').fadeOut();
        }
        else if ($('header').offset().top){
            $('header').stop().animate({backgroundColor: "rgb(255, 255, 255)"}, 'fast');
            $('.nav-bravepeach-logo').fadeIn();
        }
    });
});

$(document).on("click", function () {
    $(".traveler_cntpicker").slideUp('fast');
});
