function onOpen(evt){
    console.log("open");

    obj = {"action": "connect"};
    console.log("sending: ", obj);
    websocket.send(JSON.stringify(obj));

}
function onClose(evt){
    console.log("close");
}

function onMessage(evt){
    msg = JSON.parse(evt.data);
    console.log(msg);

    if(msg.action=='welcome'){
        my_uuid = msg.id;
    }

    if(msg.action=='spawn'){
        if(msg.object.type=='character'){
            if(msg.object.owner == my_uuid){  place_character(msg.position.x, msg.position.y);}
            else { spawn_other_character(msg.position.x, msg.position.y, msg.object.owner);}
        }
    }

    if(msg.action=='move_character'){
        move_other_character(msg.position.x, msg.position.y, msg.object.owner);
    }
}
function onError(evt){
    console.log("error");
}

var my_uuid;
var wsUri = "ws://localhost:8765";
websocket = new WebSocket(wsUri);
websocket.onopen = function(evt) { onOpen(evt) };
websocket.onclose = function(evt) { onClose(evt) };
websocket.onmessage = function(evt) { onMessage(evt) };
websocket.onerror = function(evt) { onError(evt) };
