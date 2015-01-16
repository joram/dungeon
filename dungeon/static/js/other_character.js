function _place_other_character($other_character, x, y){
    $parent = $("div[row="+y+"][col="+x+"]");
    $other_character.detach().appendTo($parent);
}

function spawn_other_character(x, y, uid, img_url){
    console.log("spawning other_character");
    $other_character = $('<img class="character" id="'+uid+'" class="square">');
    $other_character.attr('src', img_url);
    $parent = $("div[row="+y+"][col="+x+"]");
    $other_character.appendTo($parent);
}

function despawn_other_character(x, y, uid, img_url){
    $other_character = $('#'+uid);
    $other_character.detach();
}


function move_other_character(x, y, uid){
    $other_character = $('#'+uid);
    _place_other_character($other_character, x, y);
}