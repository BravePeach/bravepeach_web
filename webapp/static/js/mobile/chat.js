var webSocketBridge = new channels.WebSocketBridge();

function join_room(room_id) {
    webSocketBridge.send({
        "command": "join",
        "room": room_id
    });
}

function get_recent_chat(room_id){
    $.ajax({
        method: "POST",
        url: location.protocol + "//api.bravepeach.com/get-recent-chat",
        data: JSON.stringify({"room_id": room_id}),
        crossDomain: true,
        dataType: "json",
        contentType: "application/json"
    }).done(function(data){
        var last_timestamp = "1970-01-01";
        for (var i=0; i<data.length; i++) {
            var d = data[i];
            var date = d.timestamp.split(" ")[0];
            var msgdiv = $("#room-" + d.room_id + " .messages");
            if (date !== last_timestamp) {
                msgdiv.prepend("<div class='datediv'>"+date+"</div>");
                last_timestamp = date;
            }
            var msg = "";
            if(d.writer !== my_id) {
                msg += '<div class="profile"><img src="'+photo+'" alt="profile"></div>';
            }
            msg += "<div class='message";
            if (d.writer === my_id) {
                msg += " mine' align='right'>";
            } else {
                msg += "'>";
            }
            msg += "<span class='body'>" + d.content + "</span>" + "</div>";
            msg += "<div class='timestamp";
            if(d.writer === my_id) {
                msg += " mine' align='right'>";
            } else {
                msg += "'>";
            }
            msg += d.timestamp + "</div>";
            msgdiv.prepend(msg);
        }
        msgdiv.scrollTop(0);
    });
}

function save_data(room_id, writer, content) {
    $.ajax({
        method: "POST",
        url: location.protocol + "//api.bravepeach.com/save-chat",
        data: JSON.stringify({"room_id": room_id, "writer": writer, "content": content,
            "timestamp": new Date().toISOString().split(".")[0].replace("T", " ")}),
        crossDomain: true,
        dataType: "json",
        contentType: "application/json"
    }).done(function(data){
        console.log(data)
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
                    "<form><textarea placeholder='개인 연락처를 공개하지 마세요. 예약이 완료된 후 공개됩니다.'></textarea><button>전송</button></form>" +
                    // "<h2>" + data.title + "</h2>" +
                    "<div class='messages'></div>" +
                    "</div>"
                );
                // Hook up send button to send a message
                roomdiv.find("form").on("submit", function (e) {
                    e.preventDefault();
                    var msg = roomdiv.find("textarea").val();
                    save_data(data.join, my_id, msg);
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
                var msgdiv = $("#room-" + data.join + " .messages");
                msgdiv.scrollTop(0);
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
                    ok_msg += "<div class='timestamp";
                    if(data.uid === my_id) {
                        ok_msg += " mine' align='right'>";
                    } else {
                        ok_msg += "'>";
                    }
                    ok_msg += new Date().toISOString().split(".")[0].replace("T", " ") + "</div>";
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
            msgdiv.prepend(ok_msg);
            msgdiv.scrollTop(0);
        } else {
            console.log("Cannot handle message!");
        }
    });
    // Says if we joined a room or not by if there's a div for it
    inRoom = function (roomId) {
        return $("#room-" + roomId).length > 0;
    };
    // Helpful debugging
    webSocketBridge.socket.onopen = function () {
        console.log("Connected to chat socket");
        join_room(room_id);
    };
    webSocketBridge.socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };
});
