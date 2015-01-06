function init_dungeon(squares){
    infinitedrag = jQuery.infinitedrag("#dungeon_map", {}, {
        width: 50,
        height: 50,
        start_col: 0,
        start_row: 0,
        oncreate: function($element, x, y) {
            src = squares[x] ? squares[x][y] ? squares[x][y]['image'] : '' : '';
            $element.css('background-image', 'url(' + src + ')');
            $element.attr('class', 'square');
        }
    });
}

function center_dungeon(x, y){
    infinitedrag.center(x, y);
}