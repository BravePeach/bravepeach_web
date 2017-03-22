$(function(){
    $(".rating-img").hover(function(){
        $(".rating-img").prop("src", empty_img);
        var rating = $(this).attr("class").slice(-1);
        $(".rating-img").each(function(){
            if ($(this).attr("class").slice(-1) <= rating) {
                $(this).prop("src", full_img);
            }
        });
        $("#id_rating").val(rating);
    });
});