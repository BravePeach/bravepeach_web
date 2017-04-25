var webSocketBridge = new channels.WebSocketBridge();

// Actually, not used in real service.
function make_room(){
    var opponent = $('input[name=opponent]').val();
    $.post(make_path, {
        "opponent": opponent
    }, function(data){
        if(data.ok === true) {
            $('p.empty').remove();
            var link = '<li class="room-link" data-room-id="'+data['room_id']+'" onclick="join_room()">'+data['room_title']+'</li>';
            $('ul.rooms').append(link);
        }
    });
}

function join_room(d, room_id) {
    $(".room-link").removeClass('active');
    $(d).parent().addClass("active");
    webSocketBridge.send({
        "command": "join",
        "room": room_id
    });
}

function get_recent_chat(room_id){
    $.post("https://api.bravepeach.com/get-recent-chat",
        JSON.stringify({"room_id": room_id}),
        function(data){
            var last_date = "1970-01-01 00:00:00";
            data.forEach(function(item, index){
                console.log(item);
                // ok_msg = "<div class='message";
                // if(data.uid === my_id) {
                //     ok_msg += " mine' align='right'>";
                // } else {
                //     ok_msg += "'>";
                // }
                //
                // ok_msg +=
                //     // "<span class='username'>" + data.username + ": </span>" +
                //     "<span class='body'>" + data.message + "</span>" +
                //     "</div>";
                // if(data.uid === my_id) {
                //     $(ok_msg).addClass('mine');
                // }
            });
        });
}

function save_data(room_id, writer, content) {
    $.post("https://api.bravepeach.com/save-chat",
        JSON.stringify({"room_id": room_id, "writer": writer, "content": content}),
        function (data) {
            console.log(data);
        });
}

$(function () {
    // Correctly decide between ws:// and wss://
    // var ws_path = "/chat/stream";
    console.log("Connecting to " + ws_path);
    webSocketBridge.connect(ws_path);
    // Handle incoming messages
    webSocketBridge.listen(function(data) {
        // Decode the JSON
        // console.log("Got websocket message", data);
        // Handle errors
        if (data.error) {
            alert(data.error);
            return;
        }
        // Handle joining
        if (data.join) {
            console.log("Joining room " + data.join);
            if($("#room-"+data.join).length === 0) {
                var roomdiv = $(
                    "<div class='room' id='room-" + data.join + "'>" +
                    // "<h2>" + data.title + "</h2>" +
                    "<div class='messages'></div>" +
                    "<form><textarea></textarea><button>Send</button></form>" +
                    "</div>"
                );
                // Hook up send button to send a message
                roomdiv.find("form").on("submit", function (e) {
                    e.preventDefault();
                    var msg = roomdiv.find("input").val();
                    save_data(msg);
                    webSocketBridge.send({
                        "command": "send",
                        "room": data.join,
                        "message": msg  // roomdiv.find("input").val()
                    });
                    roomdiv.find("input").val("");
                    return false;
                });
                $("#chats").empty();
                $("#chats").append(roomdiv);
                get_recent_chat(data.join);
            }
        } else if (data.leave) {
            console.log("Leaving room " + data.leave);
            $("#room-" + data.leave).remove();
            // Handle getting a message
        } else if (data.message || data.msg_type != 0) {
            var msgdiv = $("#room-" + data.room + " .messages");
            var ok_msg = "";
            // msg types are defined in chat/settings.py
            // Only for demo purposes is hardcoded, in production scenarios, consider call a service.
            switch (data.msg_type) {
                case 0:
                    // Message
                    ok_msg = "<div class='message";
                    if(data.uid === my_id) {
                        ok_msg += " mine' align='right'>";
                    } else {
                        ok_msg += "'>";
                    }

                    ok_msg +=
                        // "<span class='username'>" + data.username + ": </span>" +
                        "<span class='body'>" + data.message + "</span>" +
                        "</div>";
                    if(data.uid === my_id) {
                        $(ok_msg).addClass('mine');
                    }
                    break;
                case 1:
                    // Warning / Advice messages
                    ok_msg = "<div class='contextual-message text-warning'>" + data.message +
                        "</div>";
                    break;
                case 2:
                    // Alert / Danger messages
                    ok_msg = "<div class='contextual-message text-danger'>" + data.message +
                        "</div>";
                    break;
                case 3:
                    // "Muted" messages
                    ok_msg = "<div class='contextual-message text-muted'>" + data.message +
                        "</div>";
                    break;
                case 4:
                    // User joined room
                    // ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                    //     " joined the room!" +
                    //     "</div>";
                    break;
                case 5:
                    // User left room
                    // ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                    //     " left the room!" +
                    //     "</div>";
                    break;
                default:
                    console.log("Unsupported message type!");
                    return;
            }
            msgdiv.append(ok_msg);
            msgdiv.scrollTop(msgdiv.prop("scrollHeight"));
        } else {
            console.log("Cannot handle message!");
        }
    });
    // Says if we joined a room or not by if there's a div for it
    inRoom = function (roomId) {
        return $("#room-" + roomId).length > 0;
    };
    // roomId = $(this).attr("data-room-id");
    // if (inRoom(roomId)) {
    //     // Leave room
    //     $(this).removeClass("joined");
    //     webSocketBridge.send({
    //         "command": "leave",
    //         "room": roomId
    //     });
    // } else {
    //     // Join room#}
    //     $(this).addClass("joined");
    //     webSocketBridge.send({
    //         "command": "join",
    //         "room": roomId
    //     });
    // }
    // Helpful debugging
    webSocketBridge.socket.onopen = function () {
        console.log("Connected to chat socket");
        $('.room-link.active').click();
    };
    webSocketBridge.socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };
});
