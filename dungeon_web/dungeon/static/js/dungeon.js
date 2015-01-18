
function init_dungeon(){
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
    $square_element = $("div[row="+y+"][col="+x+"]");
    $square_element.attr('class', 'square');
    square = get_entity(x, y, 'square');
    if(square){
       src = square.parameters.image;
       $square_element.css('background-image', 'url(' + src + ')');
    };

    get_entities(x, y).each(function(entity){
        if(entity.type != 'square'){
            if(entity.element){
                entity.element.appendTo($square_element);
            }
        }
    });

}


function add_squares(squares){

    function add_square_recursive(square){
        add_entity(square.x, square.y, 'square', '', '', square.data);
        update_square(square.x, square.y);
        add_next_square();
    }

    function add_next_square(){
        if(squares){
            setTimeout(function(){
                square = JSON.parse(squares.pop());
                add_square_recursive(square);
            }, 100);
        } else {
            adding_squares = false;
        }
    }

    add_next_square();
}