function _place_other_character($other_character, x, y){
    $parent = $("div[row="+y+"][col="+x+"]");
    $other_character.detach().appendTo($parent);
}

function spawn_other_character(x, y, uid){
    console.log("spawning other_character");
    $other_character = $('<img class="character" id="'+uid+'" class="square">');
    $other_character.attr('src', '/static/images/tiles/character.png');
    $parent = $("div[row="+y+"][col="+x+"]");
    $other_character.appendTo($parent);
}

function move_other_character(x, y, uid){
    $other_character = $('#'+uid);
    _place_other_character($other_character, x, y);
}