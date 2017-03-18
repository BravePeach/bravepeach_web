function like(e){
    if ($(e).hasClass("liked")){
        $(e).removeClass("liked").addClass("unliked")
        var url = "/delete_like";
    }
    else {
        $(e).removeClass("unliked").addClass("liked")
        var message = '<div class="like-message">' +
        '<img class="guide-image" src="/static/image/images/jinwoong.jpg" style="width: 64px; height: 64px; left:13px; top:31px">' +
        '<span class="like-message-text"> <strong>' + e.parentElement.parentElement.childNodes[3].innerHTML + '</strong>가이드를 찜 하셨습니다.<br>\'찜한 가이드\'에서 확인하실 수 있습니다.</span>' +
        '</div>';
        $('.like-message-wrapper').append(message);
        $('.like-message').last().delay(3000).fadeOut();
        var url = "/add_like";
    }

    $.ajax({
        url: url,
        type: "GET",
        data: {
            user_id: $(e).siblings("#user_id").val(),
            guide_id: $(e).siblings('#guide_id').val(),
        },
    })
}
