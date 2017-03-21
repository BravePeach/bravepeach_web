function cert_mail() {
    var mail = $("#cert-mail").val();

    if (mail_re.test(mail)) {
        $.post('/cert_mail', {mail: mail}, function(data){
            if(data.ok === true) {
                $(".cert-notice").css("display", "block");
            } else {
                swal({
                    type: "warning",
                    title: "Something is Wrong. Ask to Service Manager."
                });
            }
        });
    } else {
        swal({
            title: "Wrong email format",
            type: "error"
        });
    }
}

function cert_phone() {
    var country_num = $("#cert-country option:selected").val();
    var phone_num = $("#cert-phone-num").val();

    swal({
        type: "info",
        title: "Under Construction...",
        text: country_num + ") " + phone_num
    });
}

function cert_phone2() {
    swal({
        type: "info",
        title: "Under Construction..."
    });
    // TODO: empty all input and show cert msg
}

function edit_profile() {

    if (($("#id_password").val()===""&&$("#id_password2").val()==="") ||
        (validate_pw() && $("#id_password").val()===$("#id_password2").val())) {
        $(".hidden_submit").trigger("click");
    } else {
        swal("Invalid PW format", "Password must contains at least one alphabet/number/special character.", "error");
        $("#id_password").val("");
        $("#id_password2").val("");
        $("#id_password").focus();
    }
}

$(function(){
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

    $(".show-toggle").click(function() {
            var btn = $(this);
            if (btn.hasClass("expanded")) {
                btn.removeClass("expanded");
                $(".hidden").css("display", "none");
            } else {
                btn.addClass("expanded");
                $(".hidden").css("display", "block");
            }
        }
    );
});