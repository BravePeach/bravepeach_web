city_name_list = [];
var place_list = [];

$(function(){
    $("#id_city").placecomplete({
        tags: true,
        requestParams: {
            types: ["(regions)"]
        }
    });

    $("#id_city").on({
        'placecomplete:selected': function (evt, placeResult) {
            place_list.push(placeResult.address_components);
            city_name_list.push(placeResult['name']);
        },
        'placecomplete:cleared': function() {
            place_list.pop();
            city_name_list.pop();
        }
    });

    $("#type-all").click(function(){
        var sel = $(this).is(':checked');
        if (sel === true) {
            $("input[name=guide-type]").prop("checked", true);
        } else {
            $("input[name=guide-type]").prop("checked", false);
        }
    });
    $("#theme-all").click(function(){
        var sel = $(this).is(':checked');
        if (sel === true) {
            $("input[name=guide-theme]").prop("checked", true);
        } else {
            $("input[name=guide-theme]").prop("checked", false);
        }
    });
});

function add_block(type) {
    var target = $("#"+type+"-block").clone();
    target.removeClass("hidden-div");
    target.addClass(type+"-block");
    target.removeAttr("id");
    $("#add-"+type+"-btn").before(target);
}

function delete_block(e) {
    var target = $(e).parent();
    target.remove();
}

function submit_form(){
    if (!$("#agree-terms").is(":checked")) {
        swal({
            title: "약관에 동의해주세요",
            type: "error"
        });
        return false;
    }

    var formdata = new FormData();

    var real_name = $("#id_real_name").val();
    if (real_name === "") {
        swal({
            title: "실명을 작성해주세요",
            type: "error"
        });
        $("#id_real_name").focus();
        return false;
    }
    formdata.append("real_name", real_name);

    var is_thru = $("#is_thru").is(":checked");
    var is_local = $("#is_local").is(":checked");
    if(!(is_local || is_thru)) {
        swal({
            title: "가이드 타입을 정해주세요",
            type: "error"
        });
        $("#is_thru").focus();
        return false;
    }
    formdata.append("is_thru", is_thru);
    formdata.append("is_local", is_local);

    if(city_name_list.length === 0) {
        swal({
            title: "1개 이상의 도시를 선택해주세요",
            type: "error"
        });
        $("#s2id_id_city").focus();
        return;
    }

    var country_list = [];
    var city_list = [];
    for (var i in place_list) {
        country_list.push(place_list[i][place_list[i].length - 1]['short_name']);
        if (place_list[i][place_list[i].length - 2]) {
            city_list.push(place_list[i][place_list[i].length - 2]['short_name']);
        }
    }
    country_list = country_list.filter (function (value, index, array) {
        return array.indexOf (value) == index;
    });

    city_list = city_list.filter (function (value, index, array) {
        return array.indexOf (value) == index;
    });

    formdata.append("guide_location", JSON.stringify(city_name_list));
    formdata.append("guide_country", JSON.stringify(country_list));
    formdata.append("guide_city", JSON.stringify(city_list));

    var introduction = $("#id_introduction").val();
    if (introduction === "") {
        swal({
            title: "자기소개를 작성해주세요",
            type: "error"
        });
        $("#introduction").focus();
        return false;
    }
    formdata.append("introduction", introduction);

    var career = [];
    $(".career-block").each(function(){
        var career_date = $(this).find('.career-date').val();
        var career_company = $(this).find('.career-company').val();
        var career_info = $(this).find('.career-info').val();
        console.log([career_date, career_company, career_info]);
        if (career_date !== "" || career_company !== "" || career_info !== "") {
            career.push([career_date, career_company, career_info]);
        }
    });
    if(career.length === 0) {
        swal({
            title: "경력을 작성해주세요",
            type: "error"
        });
        $($(".career_block")[0]).focus();
        return false;
    }
    formdata.append("career", JSON.stringify(career));

    var cert = [];
    $(".certificate-block").each(function(){
        var cert_file = $(this).find('.certificate-img')[0].files[0];
        if (cert_file !== undefined) {
            cert.push(cert_file);
            formdata.append("certificate", cert_file);
        }
    });
    if (cert.length === 0) {
        swal({
            title: "자격증을 첨부해주세요",
            type: "error"
        });
        return false;
    }
    // formdata.append("certificate", cert);

    var appeal = [];
    $(".appeal-block").each(function(){
        var appeal_data = $(this).find('.appeal-link').val();
        if (appeal_data !== "") {
            appeal.push(appeal_data);
        }
    });
    if (appeal.length === 0) {
        swal({
            title: "링크를 추가해주세요",
            type: "error"
        });
        return false;
    }
    formdata.append("appeal", JSON.stringify(appeal));

    var guide_type = 0;
    if ($("#type-all").is(":checked")) {
        guide_type = parseInt($("#type-all").val());
        // guide_type = $(this).val();
    } else {
        $("input[name=guide-type]:checked").each(function () {
            guide_type += parseInt($(this).val());
        });
    }
    if (guide_type === 0) {
        swal({
            title: "1개 이상의 성격을 선택해주세요",
            type: "error"
        });
        return false;
    }
    formdata.append("guide_type", guide_type);

    var guide_theme = 0;
    if ($("#theme-all").is(":checked")) {
        guide_theme = parseInt($("#theme-all").val());
    } else {
        $("input[name=guide-theme]:checked").each(function(){
            guide_theme += parseInt($(this).val());
        });
    }
    if (guide_theme === 0) {
        swal({
            title: "1개 이상의 테마를 선택해주세요",
            type: "error"
        });
        return false;
    }
    formdata.append("guide_theme", guide_theme);

    var essay = $("#id_essay").val();
    if (essay === "") {
        swal({
            title: "가이드 설명을 작성해주세요",
            type: "error"
        });
        return false;
    }
    formdata.append("essay", essay);

    var exp = [];
    $(".exp-block").each(function(){
        var exp_file = $(this).find("input")[0].files[0];
        var exp_txt = $(this).find("textarea").val();
        if (exp_file !== undefined && exp_txt !== "") {
            formdata.append("experience", exp_file);
            exp.push(exp_txt);
        }
    });
    formdata.append("exp", JSON.stringify(exp));

    $.ajax({
        url: volunteer_url,
        method: "POST",
        processData: false,
        contentType: false,
        data: formdata,
        success: function(data){
            // var modal = $("#modal")
            // modal.html(data);
            // var target = modal.find("div.contents-wrapper").clone();
            // modal.empty();
            // modal.html(target);
            // modal.removeClass("hidden-div");
            // $('html, body').animate({scrollTop: 0}, "fast");
            if (data['ok'] === true) {
                location.href = '../view-volunteer/'+data['vid'];
            } else {
                swal({
                    type: "error",
                    title: "Oops!",
                    text: "어머나! 관리자에게 문의하세요"
                });
            }
        }
    });
}
