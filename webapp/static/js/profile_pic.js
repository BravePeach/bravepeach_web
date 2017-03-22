var img_coord = [];
var img_url = "";

function cancel_profile(){
    $("#original_profile").prop("src", "");
    $("#original_profile").removeAttr("style");
    $("#original_profile").data('Jcrop').destroy();
    $("#profile-input").val("");
    $(".profile_modal").removeClass("activated");
}

function save_profile(){
    cancel_profile();
    $.post(profile_upload_url,
        {
            img: img_url,
            coord: img_coord
        },function(data){
        if (data['ok'] === true) {
            alert(data["url"]);
            $("#profile-image").prop("src", data["url"]);
        }
    });
}

function get_coord(c){
    img_coord = [c.x, c.y, c.x2, c.y2];
    console.log(img_coord);
}

$(function(){
    $(".profile-pic").click(function(){
        $("#profile-input").click();
    });

    $("#profile-input").change(function(){
        var formdata = new FormData();
        formdata.append("original", $("#profile-input")[0].files[0]);

        $.ajax({
            url: original_upload_url,
            processData: false,
            contentType: false,
            data: formdata,
            type: "POST",
            success: function(data){
                if (data["ok"] === true) {
                    $(".profile_modal").addClass("activated");
                    img_url = data['url'];
                    $("#original_profile").prop("src", data["url"]);
                    $("#original_profile").Jcrop({
                        addClass: "jcrop-centered",
                        aspectRatio: 1,
                        setSelect: [0, 0, 600, 600],
                        onSelect: get_coord
                    });
                }
            }
        });
    });
});