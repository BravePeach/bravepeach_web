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
      $('body').css('overflow', 'hidden')
   });

   $('.modal-exit, .delete-no').click(function () {
      $('.allover').addClass('display-none');
      $('.delete-modal').addClass('display-none');
      $('body').css('overflow', 'auto')
   });

   $('.delete-yes').click(function () {

   });

   $('.cal').fullCalendar({
       header: {
           left: 'prev,next today',
           center: 'title',
           right: 'month,agendaWeek,agendaDay'
       },
       defaultDate: '2014-06-12',
       defaultView: 'month',
   })
});