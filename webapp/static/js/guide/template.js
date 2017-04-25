function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(input).parent().css({
                'background-image': 'url(' + e.target.result + ')',
                'opacity': 1
            })
        };

        reader.readAsDataURL(input.files[0])

    }
}

function searchGuideTemp(s_id, val, page) {
    $.ajax({
        url: "/search_guide/",
        type: "GET",
        data: {
            title: val,
            page: page,
            guide_id: $('#guide_id').val(),
            s_id: s_id,
            urls: window.location.pathname
        }
        , beforeSend: function () {
            $('.search-wrapper .guide .search-result').html('');
            $('.guide-result .loading').removeClass('display-none');
        }
        , complete: function () {
            $('.guide-result .loading').addClass('display-none');
        },
        success: function (data) {
            $('#guide_search' + s_id).replaceWith(data);
            $('#guide_search' + s_id).children('.content').addClass('display-none');
            $('#guide_search' + s_id).children('.guide-result').removeClass('display-none')
        }
    })
}

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
    $('.accom').on("click", ".delete-out, .delete-no, .address-ok", function () {
        $(this).parent().hide();
        $(this).parent().next().hide();
    });

    $('span.accom, span.guide, span.product').click(function () {
        $(this).siblings().removeClass('clicked');
        $(this).addClass('clicked');
        $('.wrapper').children().addClass('display-none');
        var clickedClass = $(this).attr('class').split(' ')[0];
        $('div.' + clickedClass).removeClass('display-none');
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


    // search guide template: if click button or press enter, submit
    $('.search-wrapper .guide').on("click", ".search-button", function () {
        var s_id = $(this).parent().parent()[0].id.replace('guide_search', '');
        searchGuideTemp(s_id, $(this).prev().val(), 1);
    });

    $('.search-wrapper .guide').on("keydown", ".search-form", function (e) {
        if (e.which == 13) {
            var s_id = $(this).parent().parent()[0].id.replace('guide_search', '');
            searchGuideTemp(s_id, $(this).val(), 1);
        }
    });

    // search-guide pagination
    $('.search-wrapper .guide').on("click", ".page.active", function () {
        var page = parseInt($(this).html());
        var s_id = $(this).parents('.guide-search')[0].id.replace('guide_search', '');
        searchGuideTemp(s_id, $(this).parent().parent().children('.search-form').val(), page);
    });

    $('.search-wrapper .guide').on("click", ".page-prev", function () {
        var page = parseInt($(this).siblings('.inactive').html()) - 1;
        var s_id = $(this).parents('.guide-search')[0].id.replace('guide_search', '');
        searchGuideTemp(s_id, $(this).parent().parent().children('.search-form').val(), page);
    });

    $('.search-wrapper .guide').on("click", ".page-next", function () {
        var page = parseInt($(this).siblings('.inactive').html()) + 1;
        var s_id = $(this).parents('.guide-search')[0].id.replace('guide_search', '');
        searchGuideTemp(s_id, $(this).parent().parent().children('.search-form').val(), page);
    });

    $('.guide.search').on("click", ".result-card", function () {
        $(this).siblings().removeClass('activated');
        $(this).siblings().children('.card-selected').addClass('display-none');
        $(this).addClass('activated');
        $(this).children('.card-selected').removeClass('display-none');
    });

    $('.accom.search').on("click", ".result-card", function () {
        $(this).siblings().removeClass('activated');
        $(this).siblings().children('.card-selected').addClass('display-none');
        $(this).addClass('activated');
        $(this).children('.card-selected').removeClass('display-none');
    });

    // 템플릿 클릭하면 내용 로드하기
    $('.accom.search').on("click", ".load-button", function () {
        var accom_id = $(this).parent().siblings('input').val();
        var s_id = $(this).parents('.accom-search')[0].id.replace('accom_search', '');
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
                $('.accom-save-button').addClass('inactive');
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

    // 템플릿 클릭하면 내용 로드하기
    $('.guide.search').on("click", ".load-button", function () {
        var guide_id = $(this).parent().siblings('input').val();
        var s_id = $(this).parents('.guide-search')[0].id.replace('guide_search', '');
        var date = $('#guide_form' + s_id).parent().prev().val();
        $.ajax({
            url: "/load_guide",
            type: "GET",
            data: {
                guide_id: guide_id,
                id: s_id,
                date: date,
                urls: window.location.pathname
            },
            success: function (data) {
                $('#guide_form' + s_id).replaceWith(data);
                $('.guide-save-button').addClass('inactive');
            }
            , beforeSend: function () {
                $('#guide_form' + s_id).children('.overlay').css("display", "block");
                $('#guide_form' + s_id).children('.overlay').children('.new, .load').css("display", "none");
                $('#guide_form' + s_id).children('.overlay').children('.loading').removeClass('display-none');
                $('#guide_form' + s_id).children('.overlay').css("background", "rgba(0, 0, 0, 0.3)")
            }
            , complete: function () {
                $('#guide_form' + s_id).children('.overlay').hide();
            }
        })
    });

    // 폼 내용이 변경되었을 때만 저장 버튼 활성화
    $('div.guide, div.accom').on("keypress", "input, textarea", function () {
        var formType = $(this).parent().parent().attr('class');
        console.log(formType);
        $('.' + formType + '-save-button').removeClass('inactive');
    });

    // 가이드 이미지 업로드
    $('.guide').on("click", ".add-photo-button", function () {
        var clickedDiv = $(this);
        $(this).next().click();
        $(this).next().change(function () {
            readURL(this);
            $(this).prev().addClass('display-none')
        });
    });

    // 숙소 이미지 업로드
    $('.accom').on("click", ".add_button", function () {
        $(this).next().click();
        $(this).next().change(function () {
            readURL(this);
            $(this).prev().addClass('display-none')
        });
    });

    $('.accom').on("click", ".accom-address", function () {
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

        autocomplete = new google.maps.places.Autocomplete(modalInput[0]);
        autocomplete.bindTo('bounds', map);

        var infowindow = new google.maps.InfoWindow();

        google.maps.event.addListener(map, 'click', function (event) {
            input.siblings('.accom-save-button').addClass('activated');
            if (marker && marker.setMap) {
                marker.setMap(null);
            }
            marker = new google.maps.Marker({
                position: event.latLng,
                map: map
            });
            var geocoder = new google.maps.Geocoder;
            geocoder.geocode({'location': event.latLng}, function (results, status) {
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


    $('.guide-preview-button').click(function () {
        
    });

    // 초기화 버튼
    $('.accom-refresh-button, .guide-refresh-button, .accom-delete, .guide-delete').click(function () {
        var formType = $(this).attr('class').slice(0, 5);
        var url = "/new_" + formType + "_form";
        $.ajax({
            url: url,
            type: "GET",
            data: {
                id: 1,
                urls: window.location.pathname
            },
            success: function (data) {
                $('#' + formType + '_form1').replaceWith(data.split('<!--!>')[0]);
                //TODO: 템플릿 불러왔을때는 템플릿 아이디 집어넣기
            }
        })
    });

    $('.accom-preview-button').click(function () {
        $('.ap-title').text($('.accom-title-form').val());
        $('.ap-type').text($('.accom-type option:selected').text());
        $('.ap-locat').text($('.small_city').val() + ', ' + $('.city').val() + ', ' + $('.country').val());
        $('.ap-overlay').removeClass('display-none');
        $('body').css('overflow', 'hidden');
    });

    $('.ap-cancel').click(function () {
        $('.ap-overlay').addClass('display-none');
        $('body').css('overflow', 'auto');
    })

});