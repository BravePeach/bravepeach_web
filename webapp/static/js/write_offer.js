function searchAccom(val){
    $.ajax({
        url: "search_accom/",
        type: "GET",
        data: {title: val}
        ,beforeSend: function () {
            $('.search-wrapper .accom .search-result').html('');
            $('.loading').removeClass('display-none');
        }
        ,complete: function () {
            $('.loading').addClass('display-none');
        },
        success : function(data) {
             $('.search-wrapper .accom .search-result').html(data);
         }
    })
}

$(function () {
    // make side menu draggable
    $('.request-wrapper, .search-wrapper').draggable();

    $('.request-bar').click(function () {
        $('.request-content').slideToggle();
        if ($('.request-bar .arrow').hasClass('rotate')){
            $('.request-bar .arrow').removeClass('rotate')
        }
        else $('.request-bar .arrow').addClass('rotate');
    });

    $('.search-bar').click(function() {
        $(this).next().slideToggle();
        if ($(this).children('img').hasClass('rotate')){
            $(this).children('img').removeClass('rotate')
        }
        else $(this).children('img').addClass('rotate');
    });

    $('.big-circle.guided').first().addClass('selected');
    var select_trg = $('.selected').attr('class').split(" ")[0];
    $('.search-wrapper .' +select_trg).addClass('activated');

    $('.status-bar .big-circle.guided').click(function () {
        $(this).addClass('selected');
        $(this).siblings().removeClass('selected');
        select_trg = $('.selected').attr('class').split(" ")[0];
        $('.search-wrapper .activated').removeClass('activated');
        $('.search-wrapper .' +select_trg).addClass('activated');
    });

    $('.status-bar .text.guided').click(function () {
        $(this).prev().addClass('selected');
        $(this).prev().siblings().removeClass('selected');
        select_trg = $('.selected').attr('class').split(" ")[0];
        $('.search-wrapper .activated').removeClass('activated');
        $('.search-wrapper .' +select_trg).addClass('activated');
    });

    // if click button or press enter, submit
    $('.search-button').click(function(){
       console.log($(this).prev().val());
       searchAccom($(this).prev().val());
    });

    $('.search-form').keydown(function(e){
        if (e.which ==13){
            console.log($(this).val());
            searchAccom($(this).val());
        }
    });
});