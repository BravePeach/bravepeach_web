var mail_re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

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
        swal("Invalid PW format", "Password must contains at least one alphabet/number/special character.", "error");
        $("#id_password").val("");
        $("#id_password2").val("");
        $("#id_password").focus();
    }
}

$(function() {
    $("#id_email").on("change keyup", function () {
        $(".email-notice.email-used").css("display", "none");
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
                $(".email-notice.email-invalid").css("display", "inline-block");
            }
        }
    });

    $("#id_email").on("focusout blur", function(){
        var mail_val = $("#id_email").val();
        if (mail_val !== "" && mail_re.test(mail_val)) {
            $.post("/check_email/",
                {email: mail_val},
                function (data) {
                    if (data.ok === true && data.usable !== true) {
                        $(".email-notice.mobile-notice").css("display", "none");
                        $(".email-notice.notice-right").css("display", "none");
                        $(".email-notice.notice-wrong").css("display", "none");
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
