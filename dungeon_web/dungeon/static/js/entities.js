entities = TAFFY();

function add_entity(x, y, type, uid, element, parameters){
    entity_dict = {x:x, y:y, type:type, uid:uid, element:element, parameters:parameters};
    entities.insert(entity_dict);
}

function remove_entity(uid){
    entity = get_entities({uid:uid}).first();
    if(entity.element){
        entity.element.remove();
    }
    entities({uid:uid}).remove();
}

function update_entity(uid, x, y){
    update_dict = {}
    if(x){update_dict.x = x;}
    if(y){update_dict.y = y;}
    entities({uid:uid}).update(update_dict);
}

function get_entities(x, y, type){
    query_dict = {x:x, y:y}
    if(type){
        query_dict.type = type;
    }
    return entities(query_dict);
}

function get_entity(x, y, type, uid){
    if(uid){
        return get_entities({uid:uid}).first();
    }
    return get_entities(x, y, type).first();
}
