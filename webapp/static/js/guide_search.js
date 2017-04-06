var place_list = JSON.parse(sessionStorage.getItem("place_list"));

function changeOrder(val) {
    if (val != $('.order-active').id) {
        $('.order-active').removeClass('order-active');
        document.getElementById(val).className = 'order-active';
        filterGuide(val);
    }
}

function like(e){
    if ($(e).hasClass("liked")){
        $(e).removeClass("liked").addClass("unliked");
        var url = "/delete_like";
    }
    else {
        $(e).removeClass("unliked").addClass("liked");
        var message = '<div class="like-message">' +
        '<img class="guide-image" src="/static/image/images/jinwoong.jpg" style="width: 64px; height: 64px; left:13px; top:31px">' +
        '<span class="like-message-text"> <strong>' + e.parentElement.childNodes[3].innerHTML + '</strong>가이드를 찜 하셨습니다.<br>\'찜한 가이드\'에서 확인하실 수 있습니다.</span>' +
        '</div>';
        $('.like-message-wrapper').append(message);
        $('.like-message').last().delay(3000).fadeOut();
        var url = "/add_like";
    }

    $.ajax({
        url: url,
        type: "GET",
        data: {
            user_id: $(e).siblings("#user_id").val(),
            guide_id: $(e).siblings('#guide_id').val()
        }
    })
}

function filterGuide(sort) {
    var country_list = [];
    var city_list = [];
    for (var i in place_list) {
        country_list.push(place_list[i][place_list[i].length - 1]['short_name']);
        if (place_list[i][place_list[i].length - 2]) {
            city_list.push(place_list[i][place_list[i].length - 2]['short_name']);
        }
    }
    country_list = country_list.filter (function (value, index, array) {
        return array.indexOf (value) == index;
    });
    city_list = city_list.filter (function (value, index, array) {
        return array.indexOf (value) == index;
    });

    console.log("country: " + country_list);
    console.log("city: " + city_list);
        $.ajax({
            url: "/filtering/",
            type: "GET",
            data: {
                country: country_list,
                city: city_list,
                start_date: $('#start_date_form').val(),
                end_date: $('#end_date_form').val(),
                traveler_cnt: $('#traveler_cnt_form').val(),
                sort: sort,
            },
            success: function (data) {
                $('.guide-card-wrapper').html(data);

            },
        });
    }

$(function() {
    filterGuide('popularity');

// 가이드 검색


    $('#start_date_form, #end_date_form').change(function () {
        filterGuide($('.order-active').attr('id'));
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
            place_list.push(placeResult.address_components);
            filterGuide($('.order-active').attr('id'));
        },
        'placecomplete:cleared': function(evt) {
            place_list.pop();
            filterGuide($('.order-active').attr('id'));
        },
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

    $('#traveler_cnt_form, .arrow-down').click(function(event){
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

