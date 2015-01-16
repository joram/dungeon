squares = {}

function init_dungeon(squares){
    infinitedrag = jQuery.infinitedrag("#dungeon_map", {}, {
        width: 50,
        height: 50,
        start_col: 0,
        start_row: 0,
        oncreate: function($element, x, y) {
            update_square(x, y);
        }
    });
}

function center_dungeon(x, y){
    infinitedrag.center(x, y);
}

function update_square(x, y){
    src = squares[x] ? squares[x][y] ? squares[x][y]['image'] : '' : '';
    $element = $("div[row="+y+"][col="+x+"]");
    if(src){
       $element.css('background-image', 'url(' + src + ')');
    };
    $element.attr('class', 'square');
}

function add_square(square){
    x = square.x;
    y = square.y;
    data = square.data;

    if(x in squares == false){squares[x] = {}}
    squares[x][y] = data;
    update_square(x, y);
}

function add_squares(more_squares){
    more_squares.forEach(function(square){
        square = JSON.parse(square);
        add_square(square);
    });
}