function spawn_other_character(x, y, uid, img_url){
    console.log("spawning other_character at ("+x+","+y+")");
    $other_character = $('<img class="character" id="'+uid+'" class="square">');
    $other_character.attr('src', img_url);
    add_entity(x, y, 'character', uid, $other_character, {});
    update_square(x, y);
}

function despawn_other_character(x, y, uid, img_url){
    old_entity = get_entity(uid);
    old_x = old_entity.x;
    old_y = old_entity.y;
    remove_entity(uid);
    update_square(old_x, old_y);
    $("#"+uid).remove();  // todo: fix remove_entity to not need this
}


function move_other_character(x, y, uid){
    old_entity = get_entity(uid);
    old_x = old_entity.x;
    old_y = old_entity.y;

    update_entity(uid, x, y);
    update_square(x, y);
    update_square(old_x, old_y);
}