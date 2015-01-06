$character = $('<img class="character" id="character" class="square">');
$character.attr('src', '/static/images/tiles/character.png');

function place_character(x, y){
    $parent = $("div[row="+y+"][col="+x+"]");
    $character.detach().appendTo($parent);
    center_dungeon(x, y);
}

function is_solid(x, y){
    return squares[x] ? squares[x][y] ? squares[x][y]['solid'] : true : true;
}

function can_move(x,y){
    return !is_solid(x, y)
}

function move_character(x_offset, y_offset){
    x = parseInt($character.parent().attr('col')) + x_offset;
    y = parseInt($character.parent().attr('row')) + y_offset;
    if(can_move(x, y)){
        place_character(x, y);
        post_data = {
            action: "move_character",
            object: {owner:my_uuid},
            position: {x: x, y: y}}
        //post_data = {}
        $.post('/api/action/', post_data);
    }
}

$(document).keypress(function( event ) {
  if(event.which == 119){move_character(0, -1);}
  if(event.which == 115){move_character(0, 1);}
  if(event.which == 97){move_character(-1, 0);}
  if(event.which == 100){move_character(1, 0);}
});