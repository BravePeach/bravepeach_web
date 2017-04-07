    window.fbAsyncInit = function () {
        FB.init({
            appId: '1520837081477959',
            xfbml: true,
            version: 'v2.8'
        });
        FB.AppEvents.logPageView();
    };

(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function fb_login(){
    FB.login(function(response){
        if(response.status === 'connected') {
            console.log(response);
            $.post("/login_fb/", {"access_token": response.authResponse.accessToken},
                function(data){
                    console.log(data);
                    if(data['ok'] === true) {
                        window.location.href = '/';
                    } else{
                        swal({
                            type: "error",
                            title: "FB Login Failed",
                            text: data["msg"]
                        });
                    }
                });
        } else {
            console.log("no");
        }
    }, {scope: "email", auth_type: "reauthenticate"});
}

function ggl_login(){
    var access_token;
    gapi.auth.authorize({
        client_id: $("meta[name=google-signin-client_id]")[0].content,
        scope: "profile email openid",
        prompt: "select_account consent",
        access_type: "online"
    }, function(authResult){
        access_token = authResult['access_token'];
        $.post('/login_google/', {access_token: authResult['access_token']}, function(data){
            console.log(data);
            if(data['ok'] === true) {
                window.location.href = '/';
            } else {
                swal({
                    type: "error",
                    title: "Google Login Failed",
                    text: data["msg"]
                });
            }
        });
    });
}
