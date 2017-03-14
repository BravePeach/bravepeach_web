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