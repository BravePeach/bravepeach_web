$(function(){
    $(".tab").click(function(){
        var target_class = $(this).attr("class").split(" ")[1];
        $(".tab").removeClass("active");
        $(".tab-contents").removeClass("active");
        $(this).addClass("active");
        $(".tab-contents."+target_class).addClass("active");
    });
});
