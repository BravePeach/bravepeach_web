var place_list = [];
city_name_list = [];
var traveler_list = [0, 0, 0, 0, 0, 0];

function submit_enroll_form(){
    var country_list = [];
    var city_list = [];
    for (var i in place_list) {
        if (place_list[i].length < 5) {
            country_list.push(place_list[i][place_list[i].length - 1]['short_name']);
            if (place_list[i][place_list[i].length - 2]) {
                city_list.push(place_list[i][place_list[i].length - 2]['short_name']);
            }
        }

        else {
            country_list.push(place_list[i][place_list[i].length - 2]['short_name']);
            city_list.push(place_list[i][place_list[i].length - 3]['short_name']);
        }
    }
    country_list = country_list.filter (function (value, index, array) {
        return array.indexOf (value) == index;
    });
    city_list = city_list.filter (function (value, index, array) {
        return array.indexOf (value) == index;
    });

    $("#id_countries").val(JSON.stringify(country_list));
    $("#id_cities").val(JSON.stringify(city_list));
    $("#id_city").val(city_name_list.join());
    $("#id_age_group").val(traveler_list);
    $("#enroll-form").submit();
}

$(function() {
    $("#id_city.enroll-trip-form").placecomplete({
        tags: true,
        requestParams: {
            types: ["(regions)"]
        }
    });

    $("#id_city").on({
        'placecomplete:selected': function (evt, placeResult) {
            place_list.push(placeResult.address_components);
            city_name_list.push(placeResult['name']);
        },
        'placecomplete:cleared': function() {
            place_list.pop();
            city_name_list.pop();
        },

    });

    $('.edatepicker1, .edatepicker2').datepicker({
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
            var date1 = $('.edatepicker1').datepicker('getDate');
            var date = new Date(Date.parse(date1));
            date.setDate(date.getDate() + 1);
            var newDate = date.toDateString();
            newDate = new Date(Date.parse(newDate));
            $('.edatepicker2').datepicker("option", "minDate", newDate);
            if ($('.del-cal').hasClass('display-none')) {
                $('.del-cal').removeClass('display-none')
            }
        },
        onClose: function () {
            if ($('.edatepicker1').val() && !$('.edatepicker2').val()) {
                $('.edatepicker2').datepicker("show");
            }
        }
    });

    $('.del-cal').click(function () {
        $('.edatepicker1, .edatepicker2').val("");
        $(this).addClass('display-none')
    });


    var total_traveler = 0;

    $('.increase_button').click(function () {
        traveler_list[parseInt($(this).parent()[0].className)] ++;
        $('span:last-child', $(this).parent('div')).html(function (i, val) {
            return parseInt(val.slice(0, -1)) + 1 + '명'
        });
        total_traveler++;
        $('#traveler_cnt_main, #traveler_cnt_form, #id_age_group').attr('value', '인원 ' + total_traveler + '명')
    });

    $('.decrease_button').click(function () {
        $('span:last-child', $(this).parent('div')).html(function (i, val) {
            if (val[0] == 0) {
                return
            }
            traveler_list[parseInt($(this).parent()[0].className)] --;
            total_traveler--;
            $('#traveler_cnt_main, #traveler_cnt_form, #id_age_group').attr('value', '인원 ' + total_traveler + '명');
            return parseInt(val.slice(0, -1)) - 1 + '명'
        });
    });

    $('#id_age_group, .arrow-down, .cnt-btn').click(function (event) {
        event.stopPropagation();
        $(".traveler_cntpicker").slideToggle("fast");
    });
    $(".traveler_cntpicker").on("click", function (event) {
        event.stopPropagation();
    });

    $(".btn1").click(function () {
        if ($(".gradation-bar.btn1").hasClass("inactive")) {
            $(".gradation-bar.btn1").removeClass("inactive");
            $(".way-of-travel-button > img").attr("src", "/static/image/icon/logo_full.png");
            $('html, body').animate({scrollTop: $('.gradation-bar.btn1').offset().top - 100}, '200');
        }
        else {
            $(".gradation-bar.btn1").addClass("inactive");
            $(".way-of-travel-button > img").attr("src", "/static/image/icon/logo_empty.png");
        }
        $(".scrolling-page1").slideToggle(200);
    });

    $(".btn2").click(function () {
        if ($(".gradation-bar.btn2").hasClass("inactive")) {
            $(".gradation-bar.btn2").removeClass("inactive");
            $(".lodging-button > img").attr("src", "/static/image/icon/logo_full.png");
            $('html, body').animate({scrollTop: $('.gradation-bar.btn2').offset().top - 100}, '200')
        }
        else {
            $(".gradation-bar.btn2").addClass("inactive");
            $(".lodging-button > img").attr("src", "/static/image/icon/logo_empty.png");
        }
        $(".scrolling-page2").slideToggle(200);
    });

    $(".way-of-travel-button")
        .mousemove(function () {
            $(".way-of-travel-button > img").attr("src", "/static/image/icon/logo_full.png");
            $(".enroll-trip-button-name").attr("text-shadow", "0px 1px 1px rgba(0,0,0,0.3)");
        })
        .mouseout(function () {
            if ($(".gradation-bar.btn1").hasClass("inactive")) {
                $(".way-of-travel-button > img").attr("src", "/static/image/icon/logo_empty.png")
            }
        });


    $(".lodging-button")
        .mousemove(function () {
            $(".lodging-button > img").attr("src", "/static/image/icon/logo_full.png");
        })
        .mouseout(function () {
            if ($(".gradation-bar.btn2").hasClass("inactive")) {
                $(".lodging-button > img").attr("src", "/static/image/icon/logo_empty.png")
            }
        });

    $('#theme1').change(function(){
        $("input[name$='theme']").prop('checked', $(this).prop("checked"));
    });
    $('#gt1').change(function(){
        $("input[name$='guide_type']").prop('checked', $(this).prop("checked"));
    });
    $('#location4').change(function () {
        if ($('.location-option').hasClass('display-none')) {
            $('.location-option').removeClass('display-none')
        }
        else {
            $('.location-option').addClass('display-none')
        }
    })
    $('#im6').change(function () {
        if ($('.importance-option').hasClass('display-none')) {
            $('.importance-option').removeClass('display-none')
        }
        else {
            $('.importance-option').addClass('display-none')
        }
    })

});

$(document).on("click", function () {
    $(".traveler_cntpicker").slideUp('fast');
});
