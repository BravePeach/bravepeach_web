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

$(function(){
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