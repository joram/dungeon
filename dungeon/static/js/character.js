$character = $('<img id="character" class="square">');
$character.attr('src', '/static/images/tiles/character.png');

function place_character(x, y){
    $parent = $("div[row="+y+"][col="+x+"]");
    $character.detach().appendTo($parent);
}

function move_character(x_offset, y_offset){
    x = parseInt($character.parent().attr('col')) + x_offset;
    y = parseInt($character.parent().attr('row')) + y_offset;
    if(square_types[x][y] == "empty"){
        console.log("can move to ("+x+","+y+")");
        place_character(x, y);
        center_dungeon(x, y);
    } else {
        console.log("can't move to ("+x+","+y+")");
    }
}

function init_character(){
    place_character(0,0);
    center_dungeon(0,0);
}

$(document).keypress(function( event ) {
  if(event.which == 119){move_character(0, -1);}
  if(event.which == 115){move_character(0, 1);}
  if(event.which == 97){move_character(-1, 0);}
  if(event.which == 100){move_character(1, 0);}
});