var off_days = [];

Array.prototype.contains = function(obj) {
    var i = this.length;
    while (i--) {
        if (this[i] == obj) {
            return true;
        }
    }
    return false;
};


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

   var evt_list = [];

   $('.fixed-trip .trip-card-wrapper, .ended-trip .trip-card-wrapper').each(function(){
       var number = 0;
       for (var i=1; i<=7; i+=3){
           number += parseInt($(this).children('.traveler-num').text().split(' ')[i].slice(0,-1));
       }
       number += '명';
       var title = $(this).children('.user-name').text() + ' / ' + number + ' / ' + $(this).children('.travel-city').text().replace(/\s/g, '').replace(/\//g, ',');
       var start = $(this).children('.travel-date').text().split(' - ')[0].replace(/\//g, '-');
       var end = $(this).children('.travel-date').text().split(' - ')[1].replace(/\//g, '-') + " 20:00:00";
       if ($(this).parent().hasClass('fixed-trip')) {
           var color = "#e64c47";
       }

       else {
           var color = "#f2ad8a";
       }
	   var temp = {
	       "title": title,
           "start": start,
           "end": end,
           "color": color
       };
	   evt_list.push(temp)
   });

   $('.cal').fullCalendar({
       header: {
           left: 'prev',
           center: 'title',
           right: 'next'
       },
       selectable: true,
       selectHelper: true,
       defaultView: 'month',
       events: evt_list,
       selectOverlap: function(event) {
           return event.rendering === 'background';
       },
       select: function (start, end, jsEvent, view) {
           off_days = [];
           $(".cal").fullCalendar('clientEvents', 'off_day').forEach(function(element){
               off_days.push(element.start);
           });

           console.log(off_days.contains(start));
           if (event.rendering === 'background') {
               $(".cal").fullCalendar('removeEvent', event)
           }

           else {
               while(start.diff(end) < 0) {
                   if (!off_days.contains(start)) {
                       $(".cal").fullCalendar('addEventSource', [{
                           id: 'off_day',
                           start: start,
                           rendering: 'background',
                           block: true,
                           color: '#d4d4d4'
                       },]);
                   }
                   start.add(1, 'days')
               }

               $(".cal").fullCalendar("unselect");
           }
        },
   })
});