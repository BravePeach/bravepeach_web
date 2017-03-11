/**
 * Created by sunmoon on 17. 3. 1.
 */
// 정렬 기준 바꾸기
function changeOrder(val) {
    if (val != $('.order-active').id) {
        $('.order-active').removeClass('order-active');
        document.getElementById(val).className = 'order-active';
        filterGuide(val)
    }
}


// 가이드 검색
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
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

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
        if ($('.datepicker1').val() && !$('.datepicker2').val()){
            $('.datepicker2').datepicker("show")
        }
    }
});

$('#search_location1').click(function () {
    window.location.href = "/guide_search";
    $('#location_form').attr('value', '보라카이')
});


// var input = document.getElementById('location_form');
// var options = {
//     types: ['(regions)'],
//
// };
//
// autocomplete = new google.maps.places.Autocomplete(input, options);


    function extractor(query) {
        var result = /([^\/]+)$/.exec(query);
        if(result && result[1])
            return result[1].trim();
        return '';
    }
    var addressPicker = new AddressPicker({autocompleteService: {types: ['(regions)']}});


    $('#location_form').typeahead(null, {
        displayKey: 'description',
        source: addressPicker.ttAdapter(),
        change: function(item) {
            return this.$element.val().replace(/[^\/]*$/,'')+item+'/';
        },
        matcher: function (item) {
          var tquery = extractor(this.query);
          if(!tquery) return false;
          return ~item.toLowerCase().indexOf(tquery.toLowerCase())
        },
        highlighter: function (item) {

          var query = extractor(this.query).replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&')
          return item.replace(new RegExp('(' + query + ')', 'ig'), function ($1, match) {
            return '<strong>' + match + '</strong>'
          })
        }
    });



//$('#location_form').typeahead(null, {
  //  displayKey: 'description',
  //  source: addressPicker.ttAdapter()
//});

addressPicker.bindDefaultTypeaheadEvent($('#location_form'))

$(addressPicker).on('addresspicker:selected', function (event, result) {
    console.log(result.nameForType('country'))
    console.log("form submitted")
    console.log($('#location_form').val())
    filterGuide($('.order-active').attr('id'));
})


var input_main = document.getElementById('location_form_main');
var options_main = {};

autocomplete_main = new google.maps.places.SearchBox(input_main, options_main);

// 인원 증가
var total_traveler = 0;
$('.increase_button').click(function () {
    $('span:first-child', $(this).parent('div')).html(function (i, val) {
        return parseInt(val.slice(0, -1)) + 1 + '명'
    });
    total_traveler++;
    $('#traveler_cnt_main, #traveler_cnt_form').attr('value', '인원 ' + total_traveler + '명')
});

$('.decrease_button').click(function () {
    $('span:first-child', $(this).parent('div')).html(function (i, val) {
        if (val[0] == 0) {
            return
        }
        total_traveler--;
        $('#traveler_cnt_main, #traveler_cnt_form').attr('value', '인원 ' + total_traveler + '명');
        return parseInt(val.slice(0, -1)) - 1 + '명'
    });
});

$('#traveler_cnt_main, .arrow-down, #traveler_cnt_form').click(function () {
    $('.traveler_cntpicker').slideToggle(200)
});

// 가이드 검색 정렬
function orderGuide(value) {
    console.log(value)
};


// 버튼 클릭시 페이지 펼치기
$(".btn1").click(function () {
    if ($(".gradation-bar.btn1").hasClass("inactive")) {
        $(".gradation-bar.btn1").removeClass("inactive");
        $(".way-of-travel-button > img").attr("src", "/static/image/icon/logo_full.png");
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
    }
    else {
        $(".gradation-bar.btn2").addClass("inactive");
        $(".lodging-button > img").attr("src", "/static/image/icon/logo_empty.png");
    }
    $(".scrolling-page2").slideToggle(200);
});

$(".btn3").click(function () {
    if ($(".gradation-bar.btn3").hasClass("inactive")) {
        $(".gradation-bar.btn3").removeClass("inactive");
        $(".guide-button > img").attr("src", "/static/image/icon/logo_full.png");
    }
    else {
        $(".gradation-bar.btn3").addClass("inactive");
        $(".guide-button > img").attr("src", "/static/image/icon/logo_empty.png");
    }
    $(".scrolling-page3").slideToggle(200);
});


// 복숭아 버튼 호버시 그림 바꾸고 글자에 그림자 넣기
// 중복을 줄일수 없을까?
$(".way-of-travel-button")
    .mousemove(function () {
        $(".way-of-travel-button > img").attr("src", "/static/image/icon/logo_full.png");
        $(".enroll-trip-button-name").attr("text-shadow", "0px 1px 1px rgba(0,0,0,0.3)");
    })
    .mouseout(function () {
        // 클릭을 안했을때만 빈 그림으로 바꾼다.
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


$(".guide-button")
    .mousemove(function () {
        $(".guide-button > img").attr("src", "/static/image/icon/logo_full.png");
    })
    .mouseout(function () {
        if ($(".gradation-bar.btn3").hasClass("inactive")) {
            $(".guide-button > img").attr("src", "/static/image/icon/logo_empty.png")
        }
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

$(window).scroll(function (event) {
   var windowTop = $(this).scrollTop();
     if (windowTop >= $("footer").offset().top) {
        $(".enroll-trip-button").addClass("fixed");
      } else {
        $(".enroll-trip-button").removeClass("fixed");
      }
});
