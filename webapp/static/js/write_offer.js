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

var rgx1 = /\D/g;  // /[^0-9]/g 와 같은 표현
var rgx2 = /(\d+)(\d{3})/;

function getNumber(obj){

     var num01;
     var num02;
     num01 = obj.value;
     num02 = num01.replace(rgx1,"");
     num01 = setComma(num02);
     obj.value =  num01;

}

function setComma(inNum){

     var outNum;
     outNum = inNum;
     while (rgx2.test(outNum)) {
          outNum = outNum.replace(rgx2, '$1' + ',' + '$2');
      }
     return outNum;

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

    // 견적서 폼 지우기
    $('.cost.template').on("click", ".cost-delete", function () {
        $(this).next().show();
        $(this).next().next().show();
    });

    $('.cost.template').on("click", ".delete-out, .delete-no, .address-ok", function () {
        $(this).parent().hide();
        $(this).parent().next().hide();
    });

    $('.cost.template').on("click", ".delete-ok", function () {
        $(this).parent().hide();
        $(this).parent().next().hide();
        $(this).parents('.cost-form-wrapper').remove();
    });

    // load new cost form
    $('.cost-add-button').click(function () {
        if ($('.cost-form-wrapper').length) {
            var f_id = parseInt($('.cost-form-wrapper').last()[0].id.replace('cost_form', '')) + 1;
        }

        else var f_id = 1;

        $.ajax({
            url: "new_cost_form/",
            type: "GET",
            data: {id: f_id},
            success: function (data) {
                $('.cost.template .wrapper').append(data);
            }
        })
    });


});