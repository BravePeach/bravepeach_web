city_list = [];

function fixGuideButton() {
    var container = $('.guide-button');
    var maxTop = $('footer').offset().top - container.outerHeight() - 26.5;
    var scrollVal = $(document).scrollTop() + $(window).height() - 120;

    if (scrollVal > maxTop) {
        container.css('top', maxTop);
    }

    else {
        container.stop().animate({top: scrollVal}, '100');
    }
}

function filterTrip(sort) {
    console.log(city_list);
    $.ajax({
        url: "/trip_filtering/",
        type: "GET",
        data: {
            location: city_list,
            start_date: $('#start_date_form').val(),
            end_date: $('#end_date_form').val(),
            traveler_cnt: $('#traveler_cnt_form').val(),
            sort: sort
        }
        ,beforeSend: function () {
            $('.req-card-wrapper').html('');
            $('.loading').removeClass('display-none');
        }
        ,complete: function () {
            $('.loading').addClass('display-none');
        }
        ,success: function (object) {
            console.log(object);
            var user = object[object.length - 1];
            $('.guide-card-wrapper').html("");
            $('.search-filter-result').html(object.length - 1);
            for (var i = 0; i < object.length - 1; i++) {

                if (object[i].is_liked) {
                    var heart_image = '<div class="like-button liked" onclick="like(this)"></div>'
                }
                else {
                    var heart_image = '<div class="like-button unliked" onclick="like(this)"></div>'
                }

                if (object[i].trans_guided) {
                    var trans = '<div class="trans"><div class="guide-activated"></div><span>이동수단</span></div>'
                }
                else {
                    var trans = '<div class="trans"><div class="guide-deactivated"></div><span>이동수단</span></div>'
                }

                if (object[i].accom_guided) {
                    var accom = '<div class="accom"><div class="guide-activated"></div><span>숙소</span></div>'
                }
                else {
                    var accom = '<div class="accom"><div class="guide-deactivated"></div><span>숙소</span></div>'
                }

                if (object[i].guide_guided) {
                    var guide = '<div class="guide"><div class="guide-activated"></div><span>가이드</span></div>'
                }
                else {
                    var guide = '<div class="guide"><div class="guide-deactivated"></div><span>가이드</span></div>'
                }


                var req_card = '<div class="req-card">' +

                    '<input type="hidden" id="guide_id" value="' + user + '" name="guide_id">' +
                    '<input type="hidden" id="request_id" value="' + object[i].id + '" name="request_id">' +
                    '<img class="user-pic" src="' + object[i].profile_pic + '" >' +
                    '<div class="user-name">' + object[i].name + '</div>' + trans + accom + guide +
                    '<div class="travel-date">' + object[i].travel_begin_at + ' - ' + object[i].travel_end_at + '</div>' +
                    '<div class="travel-city">' + object[i].city + '</div>' +
                    '<div class="traveler-num">' + '성인 ' + object[i].adult_traveler + '명 | 아동' + object[i].child_traveler + '명 | 유아' + object[i].toddler_traveler + '명</div>' +
                    '<div class="cost">' + '희망 경비 ' + '<span>' + object[i].cost + '</span>' + ' 만원' + '</div>' +
                    '<a class="offer-button" href="/guide/write_offer/' + object[i].id + '">' + '견적서 작성하기' + '</a>' + heart_image +
                    '</div>';

                $('.req-card-wrapper').append(req_card);
            }
        }
        ,

        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius'data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#'class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
    ;
}


$(function () {
    $(window).scroll(function () {
        if ($('header').offset().top < 204) {
            $('header').stop().animate({backgroundColor: "rgba(255, 255, 255, 0)"}, 'fast');
        }
        else if ($('header').offset().top) {
            $('header').stop().animate({backgroundColor: "rgb(255, 255, 255)"}, 'fast');
        }
    });

    fixGuideButton();
    $('.guide-button').fadeIn('slow');
    $(document).scroll(function () {
        $('.guide-button').stop().fadeIn('slow');
        fixGuideButton();
    });

    $('.guide-tab').click(function () {
        $(this).siblings().removeClass('activated');
        $(this).addClass('activated');
    });

    filterTrip('popularity');

// 가이드 검색


    $('#start_date_form, #end_date_form').change(function () {
        filterTrip($('.order-active').attr('id'));
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
                filterTrip($('.order-active').attr('id'));
            }
        },
        onClose: function () {
            if ($('.datepicker1').val() && !$('.datepicker2').val()) {
                $('.datepicker2').datepicker("show")
            }
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
            console.log(placeResult);
            city_list.push(placeResult['name']);
            filterTrip($('.order-active').attr('id'));
        },
        'placecomplete:cleared': function (evt, placeResult) {
            console.log(placeResult);
            city_list.pop();
            filterTrip($('.order-active').attr('id'));
        }
    });


// 인원 증가
    var total_traveler = 0;
    $('.increase_button').click(function () {
        $('span:first-child', $(this).parent('div')).html(function (i, val) {
            return parseInt(val.slice(0, -1)) + 1 + '명'
        });
        total_traveler++;
        $('#traveler_cnt_form').attr('value', '인원 ' + total_traveler + '명')
    });

    $('.decrease_button').click(function () {
        $('span:first-child', $(this).parent('div')).html(function (i, val) {
            if (val[0] == 0) {
                return
            }
            total_traveler--;
            $('#traveler_cnt_form, #id_age_group').attr('value', '인원 ' + total_traveler + '명');
            return parseInt(val.slice(0, -1)) - 1 + '명'
        });
    });

    $('#traveler_cnt_form, .arrow-down').click(function (event) {
        console.log("clicked")
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
