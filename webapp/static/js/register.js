function validate_pw() {
    var pw_re = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,20}$/;
    var pw_val = $("#id_password").val();
    return (pw_val.length !== 0 && pw_re.test(pw_val));
}

function submit_register_form() {
    var form = $("#register-form");
    if (validate_pw()) {
        form.submit();
    } else {
        alert("Invalid PW form");
        $("#id_password").val("");
        $("#id_password2").val("");
        $("#id_password").focus();
    }
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

$(function() {
    $("#id_email").on("change keyup", function () {
        $(".email-notice.email-used").css("display", "none");
        var mail_re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var mail_val = $("#id_email").val();
        if (mail_val === "") {
            $(".email-notice").css("display", "inline-block");
            $(".email-notice.notice-right").css("display", "none");
            $(".email-notice.notice-wrong").css("display", "none");
        } else {
            if (mail_re.test(mail_val)) {
                $(".email-notice.mobile-notice").css("display", "none");
                $(".email-notice.notice-right").css("display", "inline-block");
                $(".email-notice.notice-wrong").css("display", "none");
            } else {
                $(".email-notice.mobile-notice").css("display", "none");
                $(".email-notice.notice-right").css("display", "none");
                $(".email-notice.notice-wrong").css("display", "inline-block");
            }
        }
    });

    $("#id_email").on("focusout, blur", function(){
        var mail_re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var mail_val = $("#id_email").val();
        if (mail_val !== "" && mail_re.test(mail_val)) {
            $.post("/check_email/",
                {
                    email: mail_val,
                    csrfmiddlewaretoken: getCookie("csrftoken")
                }, function (data) {
                    if (data.ok === true && data.usable !== true) {
                        $(".email-notice.mobile-notice").css("display", "none");
                        $(".email-notice.notice-right").css("display", "none");
                        $(".email-notice.email-used").css("display", "inline-block");
                    }
                });
        }
    });

    $("#id_password2").on("change keyup", function(){
        var pw_val = $("#id_password").val();
        var pw_val2 = $("#id_password2").val();

        if (pw_val === "" || pw_val2 === "") {
            $(".pw-notice").css("display", "inline-block");
            $(".pw-notice.notice-right").css("display", "none");
            $(".pw-notice.notice-wrong").css("display", "none");
        } else {
            if (pw_val === pw_val2) {
                $(".pw-notice.mobile-notice").css("display", "none");
                $(".pw-notice.notice-right").css("display", "inline-block");
                $(".pw-notice.notice-wrong").css("display", "none");
            } else {
                $(".pw-notice.mobile-notice").css("display", "none");
                $(".pw-notice.notice-right").css("display", "none");
                $(".pw-notice.notice-wrong").css("display", "inline-block");
            }
        }
    });
});
