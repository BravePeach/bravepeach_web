$(function(){
    $(".tab").click(function(){
        var target_class = $(this).attr("class").split(" ")[1];
        $(".tab").removeClass("active");
        $(".tab-contents").removeClass("active");
        $(this).addClass("active");
        $(".tab-contents."+target_class).addClass("active");
    });
});

function request_adjust(oid) {
    $.post(adjust_request_url, {'oid': oid},
    function(data){
        if (data['ok']===true) {
            $("#request").text(data['date']);
        } else {
            swal({
                title: "Oops!",
                text: "에러가 발생했습니다.\n관리자에게 문의해주세요.\n에러코드:"+data['msg'],
                type: "error"
            })
        }
    });
}
