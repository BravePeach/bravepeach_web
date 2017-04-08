city_list = [];

function filterTrip(sort) {
    console.log(city_list);
    $.ajax({
        url: "/trip_filtering/",
        type: "GET",
        data: {
            location: city_list,
            start_date: $('#start_date_form').val(),
            end_date: $('#end_date_form').val(),
            traveler_cnt: $('#traveler_cnt_form').val(),
            sort: sort
        }
        ,beforeSend: function () {
            $('.req-card-wrapper').html('');
            $('.loading').removeClass('display-none');
        }
        ,complete: function () {
            $('.loading').addClass('display-none');
        }
        ,success: function (data) {
            $('.req-card-wrapper').html(data);
            $('.search-filter-result').html($('.req-card').length);
        },
    });
}

$(function(){
   filterTrip('popularity');

   $('.req-card-wrapper').on('click', '.offer-button', function () {
      swal({
          type: "error",
          title: "견적서 작성하기는 pc에서만 지원합니다!"
      })
   });
});