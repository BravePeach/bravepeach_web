function searchAccom(val, page){
    $.ajax({
        url: "search_accom/",
        type: "GET",
        data: {title: val,
               page: page}
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

function paginate(page){
    searchAccom($('.accom .search-form').val(), page)
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

    // search accom template: if click button or press enter, submit
    $('.accom .search-button').click(function(){
       searchAccom($(this).prev().val(), 1);
    });

    $('.accom .search-form').keydown(function(e){
        if (e.which ==13){
            searchAccom($(this).val(), 1);
        }
    });

    // // pagination
    // $('.page.active').click(function () {
    //     console.log("a");
    //     var nextPage = parseInt($('.accom-pagination .page.active').html());
    //     searchAccom($('.accom .search-form').val(), nextPage);
    // });
});