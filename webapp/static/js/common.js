var mail_re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

function validate_pw() {
    var pw_re = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,20}$/;
    var pw_val = $("#id_password").val();
    return (pw_val.length !== 0 && pw_re.test(pw_val));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function fixTripButton() {
    if($('.enroll-trip-button').offset().top + $('.enroll-trip-button').height()
                                           >= $('footer').offset().top - 70)
        $('.enroll-trip-button').css('position', 'absolute');
    if($(document).scrollTop() + window.innerHeight < $('footer').offset().top)
        $('.enroll-trip-button').css('position', 'fixed');

}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function get_alarm(type) {
    $.get(alarm_url + '?type='+type, function(data){
        if(!data['ok']) {
            console.log("alarm get fail");
        } else {
            if(data['alarm_cnt'] > 0) {
                $("#alarm").find('a.msg').text(data['alarm_cnt'] + "개의 새로운 알림이 있습니다!");
                $("#alarm").css("display", "block");
            }
        }
    });
}

function close_alarm_msg() {
    $("#alarm").css("display", "none");
}

$(function(){
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    if ($('.enroll-trip-button').length) {
        fixTripButton();
        $('.enroll-trip-button').fadeIn('slow');
        $(document).scroll(function () {
            $('.enroll-trip-button').stop().fadeIn('slow');
            fixTripButton();
        });
    }

    $('.profile_img').click(function(event){
        event.stopPropagation();
        $(".profile-dropdown").slideToggle("fast");
    });
    $(".profile-dropdown").on("click", function (event) {
        event.stopPropagation();
    });
});

$(document).on("click", function () {
    $(".profile-dropdown").slideUp('fast');
});
