function searchGuideTemp(s_id, val, page) {
    $.ajax({
        url: "search_guide/",
        type: "GET",
        data: {
            title: val,
            page: page,
            guide_id: $('#guide_id').val(),
            s_id: s_id
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


    $('.search-bar').click(function () {
        var act = $(this).siblings('.guide-search:not(.display-none)');
        act.slideToggle();
        if ($(this).children('img').hasClass('rotate')) {
            $(this).children('img').removeClass('rotate')
        }
        else $(this).children('img').addClass('rotate');
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

    // change search id
    $('.guide.template').on("click", ".guide-form-wrapper input", function () {
        var f_id = $(this).parents('.guide-form-wrapper')[0].id.replace('guide_form', '');
        $('.guide-search:not(.display-none)').addClass('display-none');
        $('#guide_search' + f_id).removeClass('display-none');
        $('.search-wrapper').animate({top: $(this).parents('.guide-form-wrapper').offset().top});
    });

    // 템플릿 클릭하면 내용 로드하기
    $('.guide.search').on("click", ".result-card", function () {
        var guide_id = $(this).children('input').val();
        var s_id = $(this).parent().parent()[0].id.replace('guide_search', '');
        $(this).siblings().removeClass('activated');
        $(this).siblings().children('.card-selected').addClass('display-none');
        $(this).addClass('activated');
        $(this).children('.card-selected').removeClass('display-none');
        $.ajax({
            url: "load_guide",
            type: "GET",
            data: {guide_id: guide_id, id: s_id},
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
            url: "new_guide_form/",
            type: "GET",
            data: {id: f_id, date: date},
            success: function (data) {
                $('.guide.template .wrapper').append(data.split('<!--!>')[0]);
                console.log(data.split('<!--!>')[1]);
                $('.guide-search').addClass('display-none');
                $('.search-wrapper .guide').append(data.split('<!--!>')[1]);
            }
        })
    });

    // if click "새로작성하기" button
    $('.guide.template').on("click", ".guide-form-wrapper .new", function () {
        $('.search-wrapper').animate({top: $(this).parent().offset().top});
        $(this).parent().hide();
    });

    //if click "불러오기" button
    $('.guide.template').on("click", ".guide-form-wrapper .load", function () {
        $('.search-wrapper').animate({top: $(this).parent().offset().top});
        $(this).parent().hide();
        console.log($(this).parent().parent()[0].id);
        var s_id = $(this).parent().parent()[0].id.replace('guide_form', '');
        console.log(s_id);
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

    // 가이드 이미지 업로드
    $('.guide.template').on("click", ".add-photo-button", function () {
        var clickedDiv = $(this);
        $(this).next().click();
        $(this).next().change(function () {
            console.log($(this)[0].files[0]);

            var formdata = new FormData();
            formdata.append("guide_photo", $(this)[0].files[0]);

            $.ajax({
                url: "/upload_guide_photo/",
                processData: false,
                contentType: false,
                data: formdata,
                type: "POST",
                success: function (data) {
                    if (data["ok"] === true) {
                        clickedDiv.next().next().val(data['url']);
                        clickedDiv.addClass('display-none');
                        clickedDiv.parent().css({
                            "background-image": 'url(' + data['url'] + ')',
                            "opacity": 1
                        });
                    }
                }
            });
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
        $('.guide.search').find('.' + data).removeClass('display-none');
    });

    // 가이드 템플릿 저장
    $('.guide.template').on("click", ".guide-save-button.activated", function () {
        var s_id = $(this).parent()[0].id.replace("guide_form", "");
        var guide_id = $('#guide_id').val();
        var templateId = $(this).siblings('.guide-id').val();
        var guideTitle = $(this).siblings('.guide-title-form').val();
        var guideContent = $(this).siblings('.guide-content').val();

        // var photoList = [];
        // for (var i = 1; i < 5; i++) {
        //     if ($(this).siblings('.guide-photo-wrapper').children('input.photo' + i.toString()).val() != "") {
        //         photoList.push($(this).siblings('.guide-photo-wrapper').children('input.photo' + i.toString()).val())
        //     }
        // }
        //
        if (guideTitle == ""){
            alert("일정 타이틀을 입력해주세요.")
        }

        else if (guideContent == ""){
            alert("일정 정보를 작성해주세요.")
        }

        else {
            $(this).removeClass('activated');

            var templateIdinput = $(this).siblings('.guide-id');
            $.ajax({
                url: "/save_guide_template/",
                type: "POST",
                data: {
                    guide_id: guide_id,
                    guide_template_id: templateId,
                    title: guideTitle,
                    content: guideContent,
                },
                success: function (data) {
                    if (data["ok"] == true) {
                        templateIdinput.val(data["new_id"]);
                        $('#guide_search' + s_id).find('.activated input').val(data["new_id"]);
                        $('#guide_search' + s_id).find('.activated .result-title').html(guideTitle);
                        // $('#guide_search' + s_id).find('.activated img')
                    }
                }
            })
        }

    });
});