function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#thumbnail-img').attr('src', e.target.result);
            $('.thumbnail').css("display", "none");
            $("#thumbnail-img").css("display", "inline-block");
        };
        reader.readAsDataURL(input.files[0]);
        console.log(input.files[0]);
    }
}

$(function(){
    $("#id_thumbnail").change(function(){
        readURL(this);
    });

    $(".thumbnail").click(function(){
        $('#id_thumbnail').click();
    });

    $("#thumbnail-img").click(function(){
        $("#id_thumbnail").click();
    });
});
