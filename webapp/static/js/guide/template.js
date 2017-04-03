function readURL(input) {
    if (input.files && input.files[0]){
        var reader = new FileReader();

        reader.onload = function (e) {
            $(input).parent().css({'background-image': 'url(' + e.target.result + ')',
                                'opacity': 1})
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
        $('.' +  formType + '-save-button').removeClass('inactive');
    });

    // 초기화 버튼
    $('.accom-refresh-button, .guide-refresh-button').click(function () {
        var formType = $(this).attr('class').slice(0,5);
        var url = "/new_" + formType + "_form";
        $.ajax({
            url: url,
            type: "GET",
            data: {id: 1},
            success: function (data) {
                $('#' + formType + '_form1').replaceWith(data.split('<!--!>')[0]);
            }
        })
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

    $('.guide-preview-button').click(function () {

    })

});