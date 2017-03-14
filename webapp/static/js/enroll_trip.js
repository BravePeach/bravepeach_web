$(function(){
    $("#id_city").placecomplete({
        tags:true,
        requestParams: {
            types: ["(cities)"]
        }
    });
});