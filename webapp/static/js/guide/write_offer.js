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
            swal({
                title: "이동수단 정보를 작성해주세요!",
                type: "error"
            })
        }
        else {
            $.ajax({
                url: "save_trans_offer/",
                type: "POST",
                data: {
                    guide_id: $('#guide_id').val(),
                    trans_info: $('.trans-form').val()
                },
                success: function () {
                    swal({
                        title: "저장되었습니다!"
                    })
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

    // save cost_offer
    $('.cost-form-button').click(function () {
        if ($('.cost-type').val() == null){
            swal({
                title: "견적서 항목을 선택해주세요!",
                type: "error"
            })
        }

        // else if ($('.cost-content[value=""]').length + $('.cost-cost[value=""]').length){
        //     swal({
        //         title: "견적서 내용을 작성해주세요!",
        //         type: "error"
        //     })
        //
        // }

        else{
            var type_id_list = [];
            var price_list = [];
            var info_list = [];
            $('.cost-form-wrapper').each(function(){
                type_id_list.push($(this).children('.cost-type').val());
                price_list.push(parseInt($(this).children('.cost-cost').val().replace(/,/g , "")));
                info_list.push($(this).children('.cost-content').val());
            });

            $.ajax({
                url: "save_cost_offer/",
                type: "POST",
                data: {
                    guide_id : $('#guide_id').val(),
                    type_id_list: type_id_list.toString(),
                    price_list: price_list.toString(),
                    info_list: info_list.toString()
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