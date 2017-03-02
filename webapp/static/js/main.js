/**
 * Created by sunmoon on 17. 3. 1.
 */

    // 가이드 검색
    function filter_guide() {
        console.log("create post is working")

        $.ajax({
            url: "filtering/",
            type: "GET",
            data: { location: $('#location_form').val(),
                    start_date: $('#start_date_form').val(),
                    end_date: $('#end_date_form').val(),
                    traveler_cnt: $('#traveler_cnt_form').val()
            },
            success: function (data) {
                console.log(data);
                console.log("success")
            },

            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    $('#location_form, #start_date_form, #end_date_form, #traveler_cnt_form').change(function () {
        console.log("form submitted")
        filter_guide();
    });

    $('.datepicker1, .datepicker2').datepicker({
                    beforeShow: function (input, inst) {
                        setTimeout(function () {
                            inst.dpDiv.css({
                                top: 240,
                                left: 220,
                            });
                        }, 0);
                    },

                    showAnim: "slideDown",
                    minDate: 0,
                    dateFormat: 'yy.mm.dd',
                    prevText: '<',
                    nextText: '>',
                    monthNames: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
                    monthNamesShort: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
                    dayNames: ['sun','mon','tue','wed','thu','fri','sat'],
                    dayNamesShort: ['sun','mon','tue','wed','thu','fri','sat'],
                    dayNamesMin: ['sun','mon','tue','wed','thu','fri','sat'],
                    showMonthAfterYear: true,
                    yearSuffix: '년',
                    onSelect: function() {
                        var date1 = $('.datepicker1').datepicker('getDate');
                        var date = new Date( Date.parse( date1 ) );
                        date.setDate( date.getDate() + 1 );
                        var newDate = date.toDateString();
                        newDate = new Date( Date.parse( newDate ) );
                        $('.datepicker2').datepicker("option","minDate",newDate);
                        console.log($('#start_date_form').val())
                        console.log($('#end_date_form').val())

                        if($('#start_date_form').val() && $('#end_date_form').val()) {
                            filter_guide();
                        }
                    },

                })


    $('#search_location1').click(function () {
        window.location.href = "/guide_search"
        $('#location_form').attr('value', '보라카이')
    });


    var input = document.getElementById('location_form');
    var options = {
    };

    autocomplete = new google.maps.places.Autocomplete(input, options);

