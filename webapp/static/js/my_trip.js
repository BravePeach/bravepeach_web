$(function(){
    $(".tab").click(function(){
        $(".tab").removeClass("active");
        $(this).addClass("active");
        var cls_list = $(this).attr("class").split(" ");
        var target_cls = cls_list[1];
        $(".tab-contents").removeClass("tab-active");
        $(".tab-contents."+target_cls).addClass("tab-active");
    });
});

function cancel_offer(oid, gname) {
    swal({
        title: "여행 취소하기",
        text: gname + " 가이드와의 여행을 정말로 취소하시겠습니까?",
        type: "warning",
        showCancelButton: true,
        cancelButtonColor: '#e64c47',
        confirmButtonColor: '#4a4a4a',
        confirmButtonText: "네",
        cancelButtonText: "아니요",
        showLoaderOnConfirm: true,
        preConfirm: function () {
            return new Promise(function (resolve) {
                $.post("/cancel_offer/", {
                    offer_id: oid,
                    csrfmiddlewaretoken: getCookie("csrftoken")
                }).done(function(data){
                    resolve([oid, data]);
                }).fail(function(err){
                    swal({type: "error", title: err});
                });
            });
        }
    }).then(function(result){
        if (result[1]["ok"] === true) {
            swal({
                type: "success",
                title:"Offer "+result[0]+" Deleted"
            });
            location.reload();
        } else {
            swal({
                type: "error",
                title: "Offer "+result[0]+" Delete Failed."
            });
        }
    });
}