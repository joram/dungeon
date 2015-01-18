function send_server(obj){
    websocket.send(JSON.stringify(obj));
}

function onOpen(evt){
    obj = {"action": "connect"};
    send_server(obj);
}
function onClose(evt){
    console.log("close");
}

function onMessage(evt){
    msg = JSON.parse(evt.data);

    if(msg.action){
//        console.log(msg.action+": "+msg);
    }

    if(msg.action=='welcome'){
        my_uuid = msg.id;
    }

    if(msg.action=='spawn'){
        if(msg.object.type=='character'){

            // spawn your character
            if(msg.object.owner == my_uuid){
              place_character(msg.position.x, msg.position.y, msg.object.img_url);}

            // spawn other character
            else {
              spawn_other_character(msg.position.x, msg.position.y, msg.object.owner, msg.object.img_url);}
        }
    }

    if(msg.action=='despawn'){
        if(msg.object.type=='character'){
            despawn_other_character(msg.position.x, msg.position.y, msg.object.owner, msg.object.img_url);
        }
    }

    if(msg.action=='move_character'){
        move_other_character(msg.position.x, msg.position.y, msg.object.owner);
    }

    if(msg.action=='update_squares'){
        add_squares(msg.squares);
    }

}
function onError(evt){
    console.log("error");
}

var my_uuid;
var wsUri = "ws://192.168.1.162:8765";
websocket = new WebSocket(wsUri);
websocket.onopen = function(evt) { onOpen(evt) };
websocket.onclose = function(evt) { onClose(evt) };
websocket.onmessage = function(evt) { onMessage(evt) };
websocket.onerror = function(evt) { onError(evt) };
