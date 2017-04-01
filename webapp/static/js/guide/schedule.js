$(function () {
   $('span.calendar, span.fixed-trip, span.ended-trip, span.canceled-trip').click(function () {
      $(this).siblings().removeClass('clicked');
      $(this).addClass('clicked');
      $('.wrapper').children().addClass('display-none');
      var clickedClass = $(this).attr('class').split(' ')[0];
      $('div.' + clickedClass).removeClass('display-none');
   });

   $('.delete-button').click(function(){
      $('.allover').removeClass('display-none');
      $('.delete-modal').removeClass('display-none');
   });

   $('.modal-exit, .delete-no').click(function () {
      $('.allover').addClass('display-none');
      $('.delete-modal').addClass('display-none');
   });

   $('.delete-yes').click(function () {

   });
});