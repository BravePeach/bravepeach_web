var city_list = [];

$(function(){
    $("#id_city").placecomplete({
        tags:true,
        requestParams: {
            types: ["(cities)"]
        }
    });

    $("#id_city").on({'placecomplete:selected': function(evt, placeResult){
        console.log(placeResult);
        city_list.push(placeResult['name']);
        console.log(city_list);
    }});
});

function submit_enroll_form(){
    $("#id_city").val(city_list.join());
    $("#id_age_group").val(traveler_list);
    $("#enroll-form").submit();
}