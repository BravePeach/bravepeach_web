Array.prototype.contains = function(obj) {
    var i = this.length;
    while (i--) {
        if (this[i].diff(obj) == 0) {
            return true;
        }
    }
    return false;
};

var off_days;

function refreshOffDays() {
    off_days = [];
    $(".cal").fullCalendar('clientEvents', 'off_day').forEach(function(element){
        off_days.push(element.start);
    });
    return off_days
}

function saveOffDays(){
    var formatedOffDays = {};
    off_days.forEach(function (off_day) {
        formatedOffDays[off_day.format('YYYY-MM-DD')] = "";
    });
    $.ajax({
        url: "save_off_days/",
        type: "POST",
        data: {
            off_day: JSON.stringify(formatedOffDays)
        },
        success: function () {
            swal({
                title: "저장되었습니다!"
            })
        },
    });
}

$(function () {
    $('span.calendar, span.fixed-trip, span.ended-trip, span.canceled-trip').click(function () {
        $(this).siblings().removeClass('clicked');
        $(this).addClass('clicked');
        $('.wrapper').children().addClass('display-none');
        var clickedClass = $(this).attr('class').split(' ')[0];
        $('div.' + clickedClass).removeClass('display-none');
    });

    $('.delete-button').click(function () {
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
    var oldOffDays = [];
    if ($('#off_day').val() != undefined) {
        oldOffDays = $('#off_day').val().replace(/: ''/g, "").replace('{', '').replace('}', '').replace(/'/g, '').split(', ');
    };

   $('.fixed-trip .trip-card-wrapper, .ended-trip .trip-card-wrapper').each(function(){
       if($(this).children().length) {
           var number = 0;
           for (var i = 1; i <= 7; i += 3) {
               number += parseInt($(this).children('.traveler-num').text().split(' ')[i].slice(0, -1));
           }
           number += '명';
           var title = $(this).children('.user-name').text() + ' / ' + number + ' / ' + $(this).children('.travel-city').text().replace(/\s/g, '').replace(/\//g, ',');
           var start = $(this).children('.travel-date').text().split(' - ')[0].replace(/\//g, '-');
           var end = $(this).children('.travel-date').text().split(' - ')[1].replace(/\//g, '-') + " 20:00:00";
           var color;
           console.log(start, end);
           if ($(this).parent().hasClass('fixed-trip')) {
               color = "#e64c47";
           }

           else {
               color = "#f2ad8a";
           }
           var evt = {
               "title": title,
               "start": start,
               "end": end,
               "color": color
           };
           evt_list.push(evt)
       }
   });

   if (oldOffDays.length) {
       oldOffDays.forEach(function (day) {
           var evt = {
               id: 'off_day',
               title: '',
               start: day,
               rendering: 'background',
               block: true,
               color: '#d4d4d4'
           };
           evt_list.push(evt)
       });
   }

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
       selectLongPressDelay: 0,
       selectOverlap: function(event) {
           return event.rendering === 'background';
       },
       select: function (start, end) {
           off_days = refreshOffDays();

               while(start.diff(end) < 0) {
                   if (!off_days.contains(start)) {
                       $(".cal").fullCalendar('addEventSource', [{
                           id: 'off_day',
                           title: '',
                           start: start,
                           rendering: 'background',
                           block: true,
                           color: '#d4d4d4'
                       },]);
                   }
                   else{
                       $(".cal").fullCalendar('removeEvents', function (evt) {
                           return evt.start.diff(start) == 0
                        });
                   }
                   start.add(1, 'days')
               }


               $(".cal").fullCalendar("unselect");

           off_days = refreshOffDays();
           if(off_days.length == 0){
               $('.cal-save-button').addClass('deactive')
           }
           else{
               $('.cal-save-button').removeClass('deactive')
           }
        },
   })
});