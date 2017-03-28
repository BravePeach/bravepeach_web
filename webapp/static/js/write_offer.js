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
        var f_id = $(this).parent()[0].id.replace('accom_form', '');
        $('.accom-search:not(.display-none)').addClass('display-none');
        $('#accom_search' + f_id).removeClass('display-none');
        $('.search-wrapper').animate({top: $(this).parent().offset().top});
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
        var f_id = $(this).parent()[0].id.replace('accom_form', '');
        $(this).parent().remove();
        $('#accom_search' + f_id).remove()
    })

});