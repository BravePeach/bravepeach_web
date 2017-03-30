function searchAccomTemp(s_id, val, page) {
    $.ajax({
        url: "search_accom/",
        type: "GET",
        data: {
            title: val,
            page: page,
            guide_id: $('#guide_id').val(),
            s_id: s_id
        }
        , beforeSend: function () {
            $('.search-wrapper .accom .search-result').html('');
            $('.accom-result .loading').removeClass('display-none');
        }
        , complete: function () {
            $('.accom-result .loading').addClass('display-none');
        },
        success: function (data) {
            $('#accom_search' + s_id).replaceWith(data);
            $('#accom_search' + s_id).children('.content').addClass('display-none');
            $('#accom_search' + s_id).children('.accom-result').removeClass('display-none')
        }
    })
}

function searchGuideTemp(val, page) {
    $.ajax({
        url: "search_guide/",
        type: "GET",
        data: {
            title: val,
            page: page,
            guide_id: $('#guide_id').val()
        }
        , beforeSend: function () {
            $('.search-wrapper .guide .search-result').html('');
            $('.loading').removeClass('display-none');
        }
        , complete: function () {
            $('.loading').addClass('display-none');
        },
        success: function (data) {
            $('.search-wrapper .guide .search-result').html(data);
        }
    })
}

function guidePaginate(page) {
    searchGuideTemp($('.guide .search-form').val(), page)
}

$(function () {

    // make side menu draggable
    $('.request-wrapper, .search-wrapper').draggable();

    $('.request-bar').click(function () {
        $('.request-content').slideToggle();
        if ($('.request-bar .arrow').hasClass('rotate')) {
            $('.request-bar .arrow').removeClass('rotate')
        }
        else $('.request-bar .arrow').addClass('rotate');
    });

    $('.search-bar').click(function () {
        var act = $(this).siblings('.accom-search:not(.display-none)');
        act.slideToggle();
        if ($(this).children('img').hasClass('rotate')) {
            $(this).children('img').removeClass('rotate')
        }
        else $(this).children('img').addClass('rotate');
    });

    $('.big-circle.guided').first().addClass('selected');
    var select_trg = $('.selected').attr('class').split(" ")[0];
    $('.search-wrapper .' + select_trg).addClass('activated');
    $('.' + select_trg + '.template').addClass('activated');

    $('.status-bar .big-circle.guided').click(function () {
        $(this).addClass('selected');
        $(this).siblings().removeClass('selected');
        select_trg = $('.selected').attr('class').split(" ")[0];
        $('.search-wrapper .activated').removeClass('activated');
        $('.search-wrapper .' + select_trg).addClass('activated');
        $('.template.activated').removeClass('activated');
        $('.' + select_trg + '.template').addClass('activated');
    });

    $('.status-bar .text.guided').click(function () {
        $(this).prev().addClass('selected');
        $(this).prev().siblings().removeClass('selected');
        select_trg = $('.selected').attr('class').split(" ")[0];
        $('.search-wrapper .activated').removeClass('activated');
        $('.search-wrapper .' + select_trg).addClass('activated');
    });

    // search accom template: if click button or press enter, submit
    $('.search-wrapper .accom').on("click", ".search-button", function () {
        var s_id = $(this).parent().parent()[0].id.replace('accom_search', '');
        searchAccomTemp(s_id, $(this).prev().val(), 1);
    });

    $('.search-wrapper .accom').on("keydown", ".search-form", function (e) {
        if (e.which == 13) {
            var s_id = $(this).parent().parent()[0].id.replace('accom_search', '');
            searchAccomTemp(s_id, $(this).val(), 1);
        }
    });

    // search-accom pagination
    $('.search-wrapper .accom').on("click", ".page.active", function () {
        var page = parseInt($(this).html());
        var s_id = $(this).parents('.accom-search')[0].id.replace('accom_search', '');
        searchAccomTemp(s_id, $(this).parent().parent().children('.search-form').val(), page);
    });

    $('.search-wrapper .accom').on("click", ".page-prev", function () {
        var page = parseInt($(this).siblings('.inactive').html()) - 1;
        var s_id = $(this).parents('.accom-search')[0].id.replace('accom_search', '');
        searchAccomTemp(s_id, $(this).parent().parent().children('.search-form').val(), page);
    });

    $('.search-wrapper .accom').on("click", ".page-next", function () {
        var page = parseInt($(this).siblings('.inactive').html()) + 1;
        var s_id = $(this).parents('.accom-search')[0].id.replace('accom_search', '');
        searchAccomTemp(s_id, $(this).parent().parent().children('.search-form').val(), page);
    });

    // change search id
    $('.accom.template').on("click", ".accom-form-wrapper input", function () {
        var f_id = $(this).parents('.accom-form-wrapper')[0].id.replace('accom_form', '');
        $('.accom-search:not(.display-none)').addClass('display-none');
        $('#accom_search' + f_id).removeClass('display-none');
        $('.search-wrapper').animate({top: $(this).parents('.accom-form-wrapper').offset().top});
    });

    // 템플릿 클릭하면 내용 로드하기
    $('.accom.search').on("click", ".result-card", function () {
        var accom_id = $(this).children('input').val();
        var s_id = $(this).parent().parent()[0].id.replace('accom_search', '');
        console.log(accom_id, s_id);
        $.ajax({
            url: "load_accom",
            type: "GET",
            data: {accom_id: accom_id, id: s_id},
            success: function (data) {
                $('#accom_form' + s_id).replaceWith(data);
            }
            , beforeSend: function () {
                $('#accom_form' + s_id).children('.overlay').css("display", "block");
                $('#accom_form' + s_id).children('.overlay').children('.new, .load').css("display", "none");
                $('#accom_form' + s_id).children('.overlay').children('.loading').removeClass('display-none');
                $('#accom_form' + s_id).children('.overlay').css("background", "rgba(0, 0, 0, 0.3)")
            }
            , complete: function () {
                $('#accom_form' + s_id).children('.overlay').hide();
            }
        })
    });

    // search guied template
    $('.guide .search-button').click(function () {
        searchGuideTemp($(this).prev().val(), 1);
    });

    $('.guide .search-form').keydown(function (e) {
        if (e.which == 13) {
            searchGuideTemp($(this).val(), 1);
        }
    });

    // save trans
    $('.trans-form-button').click(function () {
        if (!$('.trans-form').val()) {
            alert("내용을 작성해 주세요!")
        }
        else {
            $.ajax({
                url: "save_trans/",
                type: "GET",
                data: {
                    guide_id: $('#guide_id').val(),
                    trans_info: $('.trans-form').val()
                },
                success: function () {
                    $('.trans.big-circle').removeClass('selected');
                    if ($('.accom.big-circle').hasClass('guided')) {
                        $('.accom.big-circle').addClass('selected');
                        $('.search-wrapper .activated').removeClass('activated');
                        $('.search-wrapper .accom').addClass('activated');
                        $('.template.activated').removeClass('activated');
                        $('.accom.template').addClass('activated');
                    }
                    else {
                        $('.guide.big-circle').addClass('selected');
                        $('.search-wrapper .activated').removeClass('activated');
                        $('.search-wrapper .guide').addClass('activated');
                        $('.template.activated').removeClass('activated');
                        $('.guide.template').addClass('activated');

                    }
                }
            })
        }
    });

    // load new accom_form
    $('.accom-add-button').click(function () {
        if ($('.accom-form-wrapper').length) {
            var f_id = parseInt($('.accom-form-wrapper').last()[0].id.replace('accom_form', '')) + 1;
        }

        else var f_id = 1;

        $.ajax({
            url: "new_accom_form/",
            type: "GET",
            data: {id: f_id},
            success: function (data) {
                $('.accom.template .wrapper').append(data.split('<!--!>')[0]);
                console.log(data.split('<!--!>')[1]);
                $('.accom-search').addClass('display-none');
                $('.search-wrapper .accom').append(data.split('<!--!>')[1]);
            }
        })
    });

    // if click "새로작성하기" button
    $('.accom.template').on("click", ".accom-form-wrapper .new", function () {
        $('.search-wrapper').animate({top: $(this).parent().offset().top});
        $(this).parent().hide();
    });

    //if click "불러오기" button
    $('.accom.template').on("click", ".accom-form-wrapper .load", function () {
        $('.search-wrapper').animate({top: $(this).parent().offset().top});
        $(this).parent().hide();
        console.log($(this).parent().parent()[0].id);
        var s_id = $(this).parent().parent()[0].id.replace('accom_form', '');
        console.log(s_id);
        $('.accom-search:not(.display-none)').addClass('display-none');
        $('#accom_search' + s_id).removeClass('display-none');
        $('#accom_search' + s_id).children('.content').addClass('display-none');
        $('#accom_search' + s_id).children('.accom-result').removeClass('display-none');
    });

    // x 버튼 눌렀을때 폼과 검색 바 지우기.
    $('.accom.template').on("click", ".accom-delete", function () {
        $(this).next().show();
        $(this).next().next().show();
    });

    $('.accom.template').on("click", ".delete-out, .delete-no, .address-ok", function () {
        $(this).parent().hide();
        $(this).parent().next().hide();
    });

    $('.accom.template').on("click", ".delete-ok", function () {
        $(this).parent().hide();
        $(this).parent().next().hide();
        var f_id = $(this).parents('.accom-form-wrapper')[0].id.replace('accom_form', '');
        $(this).parents('.accom-form-wrapper').remove();
        $('#accom_search' + f_id).remove()
    });

    // 주소 입력창 클릭했을떄
    $('.accom.template').on("click", ".accom-address", function () {
        var modalInput = $(this).next().children('.address-modal-form');
        var input = $(this);
        var inputCountry = $(this).siblings('.country');
        var inputCity = $(this).siblings('.city');
        var inputSmallCity = $(this).siblings('.small_city');
        var inputLat = $(this).siblings('.lat');
        var inputLng = $(this).siblings('.lng');

        $(this).next().show();
        $(this).next().next().show();

        // google maps 처음 클릭 하는 거면 초기화
        if (inputLat.val() == "" && inputLng.val() == "") {
            var map = new google.maps.Map($(this).next().children('.map')[0], {
                center: {lat: -33.8688, lng: 151.2195},
                zoom: 17
            });
            var marker = new google.maps.Marker({
                map: map,
                anchorPoint: new google.maps.Point(0, -29)
            });
        }

        // 한번 도시를 선택했던적이 있으면 그 위치로
        else {
            var map = new google.maps.Map($(this).next().children('.map')[0], {
                center: {lat: parseFloat(inputLat.val()), lng: parseFloat(inputLng.val())},
                zoom: 17
            });
            var marker = new google.maps.Marker({
                position: {lat: parseFloat(inputLat.val()), lng: parseFloat(inputLng.val())},
                map: map
            })

        }
        var options = {
            types: ['(regions)']
        };

        autocomplete = new google.maps.places.Autocomplete(modalInput[0], options);
        autocomplete.bindTo('bounds', map);

        var infowindow = new google.maps.InfoWindow();

        google.maps.event.addListener(map, 'click', function(event) {
            if (marker && marker.setMap) {
                marker.setMap(null);
            }
            marker = new google.maps.Marker({
            position: event.latLng,
            map: map
            });
            var geocoder = new google.maps.Geocoder;
              geocoder.geocode({'location': event.latLng}, function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                  if (results[1]) {
                      console.log(results);
                      modalInput.val(results[results.length - 3].formatted_address);
                      input.val(results[results.length - 3].formatted_address);
                      var addressLen = results[results.length - 3].address_components.length;
                      inputCountry.val(results[results.length - 3].address_components[addressLen - 1].long_name);
                      inputCity.val(results[results.length - 3].address_components[addressLen - 2].long_name);
                      inputSmallCity.val(results[results.length - 3].address_components[addressLen -3].long_name);
                      inputLat.val(event.latLng['lat']);
                      inputLng.val(event.latLng['lng']);

                      infowindow.setContent(results[1].formatted_address);
                      infowindow.open(map, marker);

                  } else {
                    window.alert('No results found');
                  }
                } else {
                  window.alert('Geocoder failed due to: ' + status);
                }
              });

        });

        autocomplete.addListener('place_changed', function () {
            // infowindow.close();
            // marker.setVisible(false);
            var place = autocomplete.getPlace();
            // If the place has a geometry, then present it on a map.
            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
            } else {
                map.setCenter(place.geometry.location);
                map.setZoom(17);  // Why 17? Because it looks good.
            }
        });


    });

    // 숙소 이미지 업로드
    $('.accom.template').on("click", ".photo", function () {
        var clickedDiv = $(this);
        $(this).next().click();
        $(this).next().change(function () {
            console.log($(this)[0].files[0]);

            var formdata = new FormData();
            formdata.append("accom_photo", $(this)[0].files[0]);

            $.ajax({
                url: "/upload_accom_photo/",
                processData: false,
                contentType: false,
                data: formdata,
                type: "POST",
                success: function (data) {
                    if (data["ok"] === true) {
                        clickedDiv.next().next().val(data['url']);
                        clickedDiv.children().addClass('display-none');
                        clickedDiv.css({
                            "background-image": 'url(' + data['url'] + ')',
                            "opacity": 1
                        });
                    }
                }
            });
        });
    });

    // 숙소 템플릿 저장
    $('.accom.template').on("click", ".accom-save-button", function () {
        var photoList = [];
        for (var i = 1; i < 5; i++) {
            if ($(this).siblings('.accom-photo-wrapper').children('input.photo' + i.toString()).val() != "") {
                photoList.push($(this).siblings('.accom-photo-wrapper').children('input.photo' + i.toString()).val())
            }
        }
        console.log(photoList);


    });
});