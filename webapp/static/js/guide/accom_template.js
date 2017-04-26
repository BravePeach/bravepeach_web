function searchAccomTemp(s_id, val, page) {
    $.ajax({
        url: "/search_accom/",
        type: "GET",
        data: {
            title: val,
            page: page,
            guide_id: $('#guide_id').val(),
            s_id: s_id,
            urls: window.location.pathname
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


$(function () {


    $('.search-bar').click(function () {
        var act = $(this).siblings('.accom-search:not(.display-none)');
        act.slideToggle();
        if ($(this).children('img').hasClass('rotate')) {
            $(this).children('img').removeClass('rotate')
        }
        else $(this).children('img').addClass('rotate');
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
        $(this).siblings().removeClass('activated');
        $(this).siblings().children('.card-selected').addClass('display-none');
        $(this).addClass('activated');
        $(this).children('.card-selected').removeClass('display-none');
        $.ajax({
            url: "/load_accom",
            type: "GET",
            data: {
                accom_id: accom_id,
                id: s_id,
                urls: window.location.pathname
            },
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


    // load new accom_form
    $('.accom-add-button').click(function () {
        if ($('.accom-form-wrapper').length) {
            var f_id = parseInt($('.accom-form-wrapper').last()[0].id.replace('accom_form', '')) + 1;
        }

        else var f_id = 1;

        $.ajax({
            url: "/new_accom_form/",
            type: "GET",
            data: {
                id: f_id,
                urls: window.location.pathname
            },
            success: function (data) {
                $('.accom.template .wrapper').append(data.split('<!--!>')[0]);
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
        var s_id = $(this).parent().parent()[0].id.replace('accom_form', '');
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
            input.siblings('.accom-save-button').addClass('activated');
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
                      modalInput.val(results[results.length - 3].formatted_address);
                      input.val(results[results.length - 3].formatted_address);
                      var addressLen = results[results.length - 3].address_components.length;

                      if (addressLen < 5) {
                          inputCountry.val(results[results.length - 3].address_components[addressLen - 1].long_name);
                          inputCity.val(results[results.length - 3].address_components[addressLen - 2].long_name);
                          inputSmallCity.val(results[results.length - 3].address_components[addressLen - 3].long_name);
                      }
                      else{
                          inputCountry.val(results[results.length - 3].address_components[addressLen - 2].long_name);
                          inputCity.val(results[results.length - 3].address_components[addressLen - 3].long_name);
                          inputSmallCity.val(results[results.length - 3].address_components[addressLen - 4].long_name);
                      }

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
    $('.accom.template').on("click", ".add_button", function () {
        $(this).next().click();
        $(this).next().change(function () {
            readURL(this);
            $(this).prev().addClass('display-none')
        });
    });

    // 폼 내용이 변경되었을 때만 저장 버튼 활성화
    $('.accom.template').on("keypress", "input:not(.accom-date), textarea", function () {
       $(this).siblings('.accom-save-button').addClass('activated');
    });

    $('.accom.template').on("change", "select", function(){
        $(this).siblings('.accom-save-button').addClass('activated');
    });

    // 숙소 템플릿 저장
    $('.accom.template').on("click", ".accom-save-button.activated", function () {
        var formdata = new FormData();
        var s_id = $(this).parent()[0].id.replace("accom_form", "");
        var guide_id = $('#guide_id').val();
        var templateId = $(this).siblings('.accom-id').val();
        var accomType = $(this).siblings('.accom-type').val();
        var accomTitle = $(this).siblings('.accom-title-form').val();
        var accomContent = $(this).siblings('.accom-content').val();
        var country = $(this).siblings('.country').val();
        var city = $(this).siblings('.city').val();
        var smallCity = $(this).siblings('.small_city').val();
        var lat = $(this).siblings('.lat').val();
        var lng = $(this).siblings('.lng').val();

        for (var i=1; i<5; i++){
            var file = $(this).parent().find('input.photo' + i.toString())[0].files[0];
            if (file) {
                formdata.append("photo_list", file)
            }
        }
        if (accomType == null){
            swal({
                title: "숙소유형을 선택해주세요.",
                type: "error"
            })
        }

        else if (accomTitle == ""){
            swal({
                title: "숙소 타이틀을 입력해주세요.",
                type: "error"
            })
        }

        else if (country == ""){
            swal({
                title: "숙소 위치를 선택해주세요.",
                type: "error"
            })
        }

        else if (accomContent == ""){
            swal({
                title: "숙소 정보를 작성해주세요.",
                type: "error"
            })
        }

        else if(formdata['photo_list']){
            swal({
                title: "숙소사진을 적어도 한장 올려주세요.",
                type: "error"
            })
        }

        else {
            formdata.append("guide_id", guide_id);
            formdata.append("accom_template_id", templateId);
            formdata.append("type_id", accomType);
            formdata.append("title", accomTitle);
            formdata.append("content", accomContent);
            formdata.append("country", country);
            formdata.append("city", city);
            formdata.append("small_city", smallCity);
            formdata.append("lat", lat);
            formdata.append("lng", lng);
            $(this).removeClass('activated');

            var templateIdinput = $(this).siblings('.accom-id');
            $.ajax({
                url: "/save_accom_template/",
                type: "POST",
                processData: false,
                contentType: false,
                data: formdata,
                success: function (data) {
                    if (data["ok"] == true) {
                        templateIdinput.val(data["new_id"]);
                        $('#accom_search' + s_id).find('.activated input').val(data["new_id"]);
                        $('#accom_search' + s_id).find('.activated .result-title').html(accomTitle);
                        // $('#accom_search' + s_id).find('.activated img')
                        swal({
                            title: "저장되었습니다!",
                        })
                    }
                }
            })
        }

    });

    // save_accom
    $('.accom-form-button').click(function () {
        if ($('input[value=""].accom-id').length || $('.accom-save-button').hasClass('activated')) {
            swal({
                title: "새로 작성한 내용을 먼저 저장해주세요!",
                type: "error"
            })
        }

        else if ($('input.accom-date').filter(function() { return $(this).val() == "" }).length){
            swal({
                title: "숙박 일정을 입력해주세요!",
                type: "error"
            })
        }
        else {
            var accomIdArray = $("input.accom-id").map(function() { return $(this).val() }).get();
            var accomDateArray = $("input.accom-date").map(function() { return $(this).val() }).get();
            $.ajax({
                url: "save_accom_offer/",
                type: "POST",
                data: {
                    guide_id: $('#guide_id').val(),
                    accom_id: accomIdArray.toString(),
                    accom_date: accomDateArray.toString()
                },
                success: function () {
                    swal({
                        title: "저장되었습니다!"
                    })
                }
            })
        }
    });
});
