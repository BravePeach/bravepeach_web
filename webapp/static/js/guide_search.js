var city_list = []
var traveler_list = [0, 0, 0, 0, 0, 0];

    function changeOrder(val) {
        if (val != $('.order-active').id) {
            $('.order-active').removeClass('order-active');
            document.getElementById(val).className = 'order-active';
            filterGuide(val);
        }
    }
function filterGuide(sort) {
        $.ajax({
            url: "filtering/",
            type: "GET",
            data: {
                location: $('#location_form').val(),
                start_date: $('#start_date_form').val(),
                end_date: $('#end_date_form').val(),
                traveler_cnt: $('#traveler_cnt_form').val(),
                sort: sort,
            },
            success: function (object) {
                $('.guide-card-wrapper').html("");
                $('.search-filter-result').html(object.length);
                for (var i = 0; i < object.length; i++) {
                    ratingFloat = parseFloat(object[i].rating);
                    console.log(object[i]);

                    if (/^[a-zA-Z]*$/.test(object[i].first_name) == false) {
                        var name = object[i].last_name + object[i].first_name;
                    }
                    else {
                        var name = object[i].first_name + " " + object[i].last_name;
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
                    var guide_card = `
                        <div class="guide-card" style="display: none">
                            <div class="like-button" onclick="like(this.parentElement)">하트</div>
                            <span class="guide-name">` + name +
                        `</span>
                    ` + score + `
                    <span class="guide-review">
                        가이드` + object[i].pay_cnt + `건 ㅣ 후기 ` + object[i].review_num + `개
                    </span>
                        <img class="guide-image" src="/static/image/images/jinwoong.jpg">
                    <span class="guide-location">
                        뉴욕 / 워싱턴 D.C / 시카고
                    </span>
            </div>
`;

                    $('.guide-card-wrapper').append(guide_card);
                    $('.guide-card').show('slow')
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
            console.log(placeResult);
            city_list.push(placeResult['name']);
            console.log(city_list);
        },
        'placecomplete:cleared': function() {
            city_list.pop();
            console.log(city_list)
        }
    });

    // $(addressPicker).on('addresspicker:selected', function (event, result) {
    //     console.log(result.nameForType('country'))
    //     console.log("form submitted")
    //     console.log($('#location_form').val())
    //     filterGuide($('.order-active').attr('id'));
    // })


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

    $('.arrow-down, #traveler_cnt_form').click(function () {
        $('.traveler_cntpicker').slideToggle(200)
    });


// 하트 버튼 눌렀을때
    function like(guideCard) {
        message = '<div class="like-message">' +
            '<img class="guide-image" src="/static/image/images/jinwoong.jpg" style="width: 64px; height: 64px; left:13px; top:31px">' +
            '<span class="like-message-text"> <strong>' + guideCard.childNodes[3].innerHTML + '</strong>가이드를 찜 하셨습니다.<br>\'찜한 가이드\'에서 확인하실 수 있습니다.</span>' +
            '</div>';
        $('.like-message-wrapper').append(message);
        $('.like-message').last().delay(3000).fadeOut();
    }
});