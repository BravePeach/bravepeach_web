var city_list = localStorage.getItem("city_list").split(',');
console.log(localStorage.getItem("city_list"));
console.log(city_list);

function changeOrder(val) {
    if (val != $('.order-active').id) {
        $('.order-active').removeClass('order-active');
        document.getElementById(val).className = 'order-active';
        filterGuide(val);
    }
}

function like(e){
    if ($(e).hasClass("liked")){
        $(e).removeClass("liked").addClass("unliked")
        var url = "/delete_like";
    }
    else {
        $(e).removeClass("unliked").addClass("liked")
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
    console.log(city_list);
        $.ajax({
            url: "/filtering/",
            type: "GET",
            data: {
                location: city_list,
                start_date: $('#start_date_form').val(),
                end_date: $('#end_date_form').val(),
                traveler_cnt: $('#traveler_cnt_form').val(),
                sort: sort,
            },
            success: function (object) {
                console.log(object);
                var user = object[object.length - 1];
                $('.guide-card-wrapper').html("");
                $('.search-filter-result').html(object.length - 1);
                for (var i = 0; i < object.length - 1; i++) {
                    var ratingFloat = parseFloat(object[i].rating);
                    console.log(object[i]);

                    if (/^[a-zA-Z]*$/.test(object[i].first_name) == false) {
                        var name = object[i].last_name + object[i].first_name;
                    }
                    else {
                        var name = object[i].first_name + " " + object[i].last_name;
                    }

                    if (object[i].is_liked){
                        var heart_image = '<div class="like-button liked" onclick="like(this)"></div>'
                    }

                    else {
                        var heart_image = '<div class="like-button unliked" onclick="like(this)"></div>'
                    }
                    var score = '<div class="guide-score-wrapper">\n';
                    for (var j = 0; j < 5; j++) {
                        if (ratingFloat >= 1) {
                            score += '<img class="guide-score" src="/static/image/icon/logo_full.png">\n';
                            ratingFloat--;
                        }
                        else if (ratingFloat >= 0.5) {
                            score += '<img class="guide-score" src="/static/image/icon/logo_half.png">\n';
                            ratingFloat--;
                        }
                        else {
                            score += '<img class="guide-score" src="/static/image/icon/logo_empty.png">\n';
                        }
                    }
                    score += '</div>';
                    var guide_card = '<div class="guide-card">' +
                        '<input type="hidden" id="user_id" value="' + user + '" name="user_id">' +
                        '<input type="hidden" id="guide_id" value="' + object[i].id + '" name="guide_id">' +
                            heart_image +
                            '<span class="guide-name">' + name +
                        '</span>' + score +
                    '<span class="guide-review">' +
                        '가이드 ' + object[i].pay_cnt + '건 ㅣ 후기 ' + object[i].review_num + '개'+
                    '</span>' +
                        '<img class="guide-image" src="/static/image/images/jinwoong.jpg">' +
                    '<span class="guide-location">' +
                        '뉴욕 / 워싱턴 D.C / 시카고' +
                    '</span>' +
            '</div>';

                    $('.guide-card-wrapper').append(guide_card);
                }
            },

            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius'data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#'class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

$(function() {
    filterGuide('popularity');

});