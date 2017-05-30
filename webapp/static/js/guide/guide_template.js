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

$(function () {
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

    // change search id
    $('.guide.template').on("click", ".guide-form-wrapper input", function () {
        var f_id = $(this).parents('.guide-form-wrapper')[0].id.replace('guide_form', '');
        $('.guide-search:not(.display-none)').addClass('display-none');
        $('#guide_search' + f_id).removeClass('display-none');
    });

    // 템플릿 클릭하면 내용 로드하기
    $('.guide.search').on("click", ".result-card", function () {
        var guide_id = $(this).children('input').val();
        var s_id = $(this).parent().parent()[0].id.replace('guide_search', '');
        var date = $('#guide_form' + s_id).parent().prev().val();
        $(this).siblings().removeClass('activated');
        $(this).siblings().children('.card-selected').addClass('display-none');
        $(this).addClass('activated');
        $(this).children('.card-selected').removeClass('display-none');
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


    // load new guide_form
    $('.guide-add-button').click(function () {
        if ($('.guide-form-wrapper').length) {
            var f_id = parseInt($('.guide-form-wrapper').last()[0].id.replace('guide_form', '')) + 1;
        }

        else var f_id = 1;
        var date = $(this).siblings('.guide-date').val();
        $.ajax({
            url: "/new_guide_form/",
            type: "GET",
            data: {
                id: f_id,
                date: date,
                urls: window.location.pathname
            },
            success: function (data) {
                $('.guide.template .wrapper').append(data.split('<!--!>')[0]);
                $('.guide-search').addClass('display-none');
                $('.search-wrapper .guide').append(data.split('<!--!>')[1]);
            }
        })
    });

    // if click "새로작성하기" button
    $('.guide.template').on("click", ".guide-form-wrapper .new", function () {
        $(this).parent().hide();
    });

    //if click "불러오기" button
    $('.guide.template').on("click", ".guide-form-wrapper .load", function () {
        $(this).parent().hide();
        var s_id = $(this).parent().parent()[0].id.replace('guide_form', '');
        $('.guide-search:not(.display-none)').addClass('display-none');
        $('#guide_search' + s_id).removeClass('display-none');
        $('#guide_search' + s_id).children('.content').addClass('display-none');
        $('#guide_search' + s_id).children('.guide-result').removeClass('display-none');
    });

    // x 버튼 눌렀을때 폼과 검색 바 지우기.
    $('.guide.template').on("click", ".guide-delete", function () {
        $(this).next().show();
        $(this).next().next().show();
    });

    $('.guide.template').on("click", ".delete-out, .delete-no, .address-ok", function () {
        $(this).parent().hide();
        $(this).parent().next().hide();
    });

    $('.guide.template').on("click", ".delete-ok", function () {
        $(this).parent().hide();
        $(this).parent().next().hide();
        var f_id = $(this).parents('.guide-form-wrapper')[0].id.replace('guide_form', '');
        $(this).parents('.guide-form-wrapper').remove();
        $('#guide_search' + f_id).remove()
    });

    $('.guide.template').on("click", ".add-photo-button", function () {
        $(this).next().click();
        $(this).next().change(function () {
            readURL(this);
            $(this).prev().addClass('display-none')
        });
    });

    // 폼 내용이 변경되었을 때만 저장 버튼 활성화
    $('.guide.template').on("keypress", "input, textarea", function () {
       $(this).siblings('.guide-save-button').addClass('activated');
    });

    // 날짜 선택하면 다른 날짜의 폼들 숨기기
    $('.guide-date').change(function() {
        var date = $(this).val();
        $(this).next().children().addClass('display-none');
        $(this).next().children('.' + date).removeClass('display-none');
        $('.guide-search').addClass('display-none');
        $('.guide.search').find('.' + date).removeClass('display-none');
    });

    // 가이드 템플릿 저장
    $('.guide.template').on("click", ".guide-save-button.activated", function () {
        var formdata = new FormData();
        var s_id = $(this).parent()[0].id.replace("guide_form", "");
        var guide_id = $('#guide_id').val();
        var templateId = $(this).siblings('.guide-id').val();
        var guideTitle = $(this).siblings('.guide-title-form').val();
        var guideContent = $(this).siblings('.guide-content').val();

        var photo = $(this).parent().find('input.photo')[0].files[0];
        var background_img = $(this).parent().find('div.guide-photo').css('background-image');

        // 이전에 업로드했던 이미지인 경우
        if (!photo && (background_img != "none")){
            var file_url = background_img.split("\"")[1];
            formdata.append("guide_photo_url", file_url)
        }

        // 이미지 새로 업로드 하는경우
        else if (photo) {
            formdata.append("guide_photo", photo);
        }

        if (guideTitle == ""){
            swal({
                title: "일정 타이틀을 입력해주세요.",
                type: "error"
            })
        }

        else if (guideContent == ""){
            swal({
                title: "일정 정보를 입력해주세요.",
                type: "error"
            })
        }

        else {
            formdata.append("guide_id", guide_id);
            formdata.append("guide_template_id", templateId);
            formdata.append("title", guideTitle);
            formdata.append("content", guideContent);

            $(this).removeClass('activated');

            var templateIdinput = $(this).siblings('.guide-id');
            $.ajax({
                url: "/save_guide_template/",
                type: "POST",
                processData: false,
                contentType: false,
                data: formdata,
                success: function (data) {
                    if (data["ok"] == true) {
                        templateIdinput.val(data["new_id"]);
                        $('#guide_search' + s_id).find('.activated input').val(data["new_id"]);
                        $('#guide_search' + s_id).find('.activated .result-title').html(guideTitle);
                        // $('#guide_search' + s_id).find('.activated img')
                        swal({
                            title: "저장되었습니다!"
                        })
                    }
                }
            })
        }

    });

    $('.guide-form-button').click(function () {
        var missingDate
        var isMissed = false
        for (var i=0; i<$('.guide-date').children().length; i++){
            if (!$('.guide-form-wrapper').hasClass(i)) {
                isMissed=true;
                missingDate = i + 1;
                break;
            }
        }


        if ($('.guide-save-button').hasClass('activated')){
            swal({
                title: (parseInt($('.guide-save-button.activated').parent().attr('class').split(' ')[1]) + 1).toString() + "일의 새로 작성한 내용을 모두 저장해주세요!",
                type: "error"
            })
        }

        else if($('input[value=""].guide-id').length){
            swal({
                title: (parseInt($('input[value=""].guide-id').parent().attr('class').split(' ')[1]) + 1).toString() + "일의 새로 작성한 내용을 모두 저장해주세요!",
                type: "error"
            })
        }

        else if (isMissed) {
            swal({
                title: missingDate.toString() + "일 내용을 작성해주세요!",
                type: "error"
            })
        }

        else {
            var result = [];

            for (var i=0; i<$('.guide-date').children().length; i++){
                result += ($('.guide-form-wrapper.' + i).children('.guide-id').map(function() {return $(this).val()}).get() + 'dumpstring')
            }
            $.ajax({
                url: "save_guide_offer/",
                type: "POST",
                data: {
                    guide_id: $('#guide_id').val(),
                    guide_template: result.toString()
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