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
            guide_id: $(e).siblings('#guide_id').val(),
        },
    })
}

function filterGuide(sort) {
    var country_list = JSON.parse(sessionStorage.getItem("country_list"));
    var city_list = JSON.parse(sessionStorage.getItem("city_list"));
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
                $('.search-filter-result').html($('.guide-card').length);
            },
        });
    }

$(function() {
    filterGuide('popularity');

});