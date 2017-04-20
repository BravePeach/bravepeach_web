$(function () {
    $('#comment-button').click(function () {
           if($('#comment-form').val() != "") {
               $.ajax({
                   url: '/add_user_comment/',
                   type: 'POST',
                   data: {
                       content: $('#comment-form').val()
                   }
               })
           }
    });
})