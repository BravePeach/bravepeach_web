var place_list = [];
var city_name_list = [];
traveler_list = [0, 0, 0];

function guide_search_form(){
    sessionStorage.setItem("place_list", JSON.stringify(place_list));
    sessionStorage.setItem("traveler_list", JSON.stringify(traveler_list));
    $("#guide-search-form #id_city").val(city_name_list);
    $("#guide-search-form").submit();
}

$(function() {
    $( window ).scroll(function() {
        if($('header').offset().top < 204) {
            $('header').stop().animate({backgroundColor: "rgba(255, 255, 255, 0)"}, 'fast');
        }
        else if ($('header').offset().top){
            $('header').stop().animate({backgroundColor: "rgb(255, 255, 255)"}, 'fast');
        }
    });

    $("#id_city").placecomplete({
        tags: true,
        requestParams: {
            types: ["(regions)"]
        }
    });

    $("#id_city").on({
        'placecomplete:selected': function (evt, placeResult) {
            place_list.push(placeResult.address_components);
            city_name_list.push(placeResult['display_text']);
        },
        'placecomplete:cleared': function() {
            place_list.pop();
            city_name_list.pop();
        }
    });

    $('.datepicker1, .datepicker2').datepicker({
        showAnim: "slideDown",
        minDate: 0,
        dateFormat: 'yy.mm.dd',
        prevText: '<',
        nextText: '>',
        monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        monthNamesShort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        dayNames: ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
        dayNamesShort: ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
        dayNamesMin: ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
        showMonthAfterYear: true,
        yearSuffix: '년',
        onSelect: function () {
            var date1 = $('.datepicker1').datepicker('getDate');
            var date = new Date(Date.parse(date1));
            date.setDate(date.getDate() + 1);
            var newDate = date.toDateString();
            newDate = new Date(Date.parse(newDate));
            $('.datepicker2').datepicker("option", "minDate", newDate);
            if ($('#start_date_form').val() && $('#end_date_form').val()) {
                filterGuide($('.order-active').attr('id'));
            }
        },
        onClose: function () {
            if ($('.datepicker1').val() && !$('.datepicker2').val()) {
                window.setTimeout(function(){
                    $('.datepicker2').datepicker('show');
                }, 0);
            }
        }
    });
// 인원 증가
    var total_traveler = 0;

    $('.increase_button').click(function () {
        $('span', $(this).parent('div')).html(function (i, val) {
            return parseInt(val.slice(0, -1)) + 1 + '명'
        });
        if ($(this).siblings('span').hasClass('adult_num')) {
            traveler_list[0] ++;
        }
        else if ($(this).siblings('span').hasClass('child_num')) {
            traveler_list[1] ++;
        }
        else {
            traveler_list[2] ++;
        }
        total_traveler++;
        $('#traveler_cnt_main, #traveler_cnt_form, #id_age_group').attr('value', '인원 ' + total_traveler + '명')
    });

    $('.decrease_button').click(function () {
        $('span', $(this).parent('div')).html(function (i, val) {
            if (val[0] == 0) {
                return
            }
            if ($(this).hasClass('adult_num')) {
                traveler_list[0] --;
            }
            else if ($(this).hasClass('child_num')) {
                traveler_list[1] --;
            }
            else {
                traveler_list[2] --;
            }
            total_traveler--;
            $('#traveler_cnt_main, #traveler_cnt_form, #id_age_group').attr('value', '인원 ' + total_traveler + '명');
            return parseInt(val.slice(0, -1)) - 1 + '명'
        });
    });

    $('.traveler_cnt_main').click(function(event){
        event.stopPropagation();
         $(".traveler_cntpicker").slideToggle("fast");
    });
    $(".traveler_cntpicker").on("click", function (event) {
        event.stopPropagation();
    });

});

$(document).on("click", function () {
    $(".traveler_cntpicker").slideUp('fast');
});
