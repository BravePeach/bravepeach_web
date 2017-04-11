var city_list = [];
var traveler_list = [0, 0, 0, 0, 0, 0];

function submit_enroll_form(){
    $("#id_city").val(city_list.join());
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
            console.log(placeResult);
            console.log(placeResult.geometry.location.lat());
            console.log(placeResult.geometry.location.lng());
            city_list.push(placeResult['name']);
            console.log(city_list);
        }
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
        },
        onClose: function () {
            if ($('.edatepicker1').val() && !$('.edatepicker2').val()) {
                $('.edatepicker2').datepicker("show")
            }
        }
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

    $('#traveler_cnt_main, .arrow-down, #traveler_cnt_form, .trv-btn').click(function () {
        $('.traveler_cntpicker').slideToggle(200)
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