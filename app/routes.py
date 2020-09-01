from flask import make_response

from app import app
from app.controllers.bg_light_manager import add_new_bg_light, get_bg_light_by_id, update_bg_light_by_id, \
    delete_bg_light_by_id
from app.controllers.fg_light_manager import add_new_fg_light, get_fg_light_by_id, update_fg_light_by_id, \
    delete_fg_light_by_id
from app.controllers.floor_manager import add_new_floor, get_floor_by_id, update_floor_by_id, delete_floor_by_id
from app.controllers.global_settings_manager import save_new_global_settings, get_global_settings_by_id, \
    get_global_settings_data
from app.controllers.icon_manager import add_new_icon, get_icon_by_id, update_icon_by_id, delete_icon_by_id
from app.controllers.painting_manager import add_new_painting, get_painting_by_id, update_painting_by_id, \
    delete_painting_by_id
from app.controllers.pic_size_manager import add_new_pic_size, get_pic_size_by_id, update_pic_size_by_id, \
    delete_pic_size_by_id
from app.controllers.real_size_manager import add_new_real_size, get_real_size_by_id, update_real_size_by_id, \
    delete_real_size_by_id
from app.controllers.room_manager import add_new_room, get_room_by_id, update_room_by_id, delete_room_by_id
from app.controllers.texture_manager import add_new_texture, get_texture_by_id, update_texture_by_id, \
    delete_texture_by_id, get_default_room_texture, update_default_room_texture, get_default_ceiling_texture, \
    update_default_ceiling_texture, get_default_wall_texture, update_default_wall_texture
from app.controllers.user_manager import user_login, user_register, get_user_id_remotely
from app.controllers.wall_manager import add_new_wall, get_wall_by_id, update_wall_by_id, delete_wall_by_id


# Ref: https://stackoverflow.com/questions/25860304/how-do-i-set-response-headers-in-flask

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    resp = make_response('Welcome to 3D Gallery')
    return add_headers(resp)


# ==================================   Defaults  ==================================
@app.route('/get_room_texture', methods=['POST', 'GET'])
def get_room_texture():
    """
    uuid = fields.Str(required=True)
    :return {'result_code': 0, 'error_message': '', 'textureData': texture_dict}
    """
    if check_auth_header_secret():
        resp = get_default_room_texture()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_room_texture', methods=['PUT'])
def update_room_texture():
    """
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return {'result_code': 0, 'error_message': '', 'texture_id': id}
    """
    if check_auth_header_secret():
        resp = update_default_room_texture()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_ceiling_texture', methods=['POST', 'GET'])
def get_ceiling_texture():
    """
    uuid = fields.Str(required=True)
    :return {'result_code': 0, 'error_message': '', 'textureData': texture_dict}
    """
    if check_auth_header_secret():
        resp = get_default_ceiling_texture()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_ceiling_texture', methods=['PUT'])
def update_ceiling_texture():
    """
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return {'result_code': 0, 'error_message': '', 'texture_id': id}
    """
    if check_auth_header_secret():
        resp = update_default_ceiling_texture()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_wall_texture', methods=['POST', 'GET'])
def get_wall_texture():
    """
    uuid = fields.Str(required=True)
    :return {'result_code': 0, 'error_message': '', 'textureData': texture_dict}
    """
    if check_auth_header_secret():
        resp = get_default_wall_texture()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_wall_texture', methods=['PUT'])
def update_wall_texture():
    """
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return {'result_code': 0, 'error_message': '', 'texture_id': id}
    """
    if check_auth_header_secret():
        resp = update_default_wall_texture()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   User  ==================================
@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    """
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    :return {'result_code': 0, 'error_message': '', 'uuid': temp_uuid}
    """
    if check_auth_header_secret():
        resp = user_login()
        return resp
    else:
        return 'unknown package!!!'


# @app.route('/admin_register', methods=['POST'])
# def admin_register():
#     """
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)
#     language = fields.Str(required=False)
#     status = fields.Int(required=True)
#     :return {'result_code': 0, 'error_message': '', 'uuid': temp_uuid}
#     """
#     if check_auth_header_secret():
#         resp = user_register()
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#         resp.headers['Access-Control-Allow-Headers'] = 'Accept, X-Access-Token, X-Application-Name, X-Request-Sent-Time'
#         resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
#         resp.headers['Access-Control-Allow-Credentials'] = 'true'
#         return resp
#     else:
#         return 'unknown package!!!'


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    :return {'result_code': 0, 'error_message': '', 'uuid': temp_uuid}
    """
    if check_auth_header_secret():
        resp = user_login()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/register', methods=['POST'])
def register():
    """
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    language = fields.Str(required=False)
    status = fields.Int(required=True)
    :return {'result_code': 0, 'error_message': '', 'uuid': temp_uuid}
    """
    if check_auth_header_secret():
        resp = user_register()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/login_remotely', methods=['GET', 'POST'])
def login_remotely():
    """
    key = fields.Str(required=True)
    :return {'result_code': 0, 'error_message': '', 'uuid': temp_uuid}s
    """
    if check_auth_header_secret():
        resp = get_user_id_remotely()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Floor  ==================================
@app.route('/add_floor', methods=['POST'])
def add_floor():
    """
    name = fields.Str(required=True)
    uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floor_id': floor.id}
    """
    if check_auth_header_secret():
        resp = add_new_floor()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_floor', methods=['POST', 'GET'])
def get_floor():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floorData': floor_dict}
    """
    if check_auth_header_secret():
        resp = get_floor_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_floor', methods=['PUT'])
def update_floor():
    """
    name = fields.Str(required=True)
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floor_id': floor.id}
    """
    if check_auth_header_secret():
        resp = update_floor_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_floor', methods=['DELETE'])
def delete_floor():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floor_id': floor.id}
    """
    if check_auth_header_secret():
        resp = delete_floor_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Room  ==================================
@app.route('/add_room', methods=['POST'])
def add_room():
    """
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)
    uuid = fields.Str(required=True)
    floor_id = fields.Int(required=True)
    :return {'result_code': 0, 'error_message': '', 'room_id': room.id}
    """
    if check_auth_header_secret():
        resp = add_new_room()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_room', methods=['POST', 'GET'])
def get_room():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'roomData': room_dict}
    """
    if check_auth_header_secret():
        resp = get_room_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_room', methods=['PUT'])
def update_room():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)
    floor_id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'room_id': room.id}
    """
    if check_auth_header_secret():
        resp = update_room_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_room', methods=['DELETE'])
def delete_room():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'room_id': room.id}
    """
    if check_auth_header_secret():
        resp = delete_room_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Wall  ==================================
@app.route('/add_wall', methods=['POST'])
def add_wall():
    """
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)
    uuid = fields.Str(required=True)
    room_id = fields.Int(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)
    :return {'result_code': 0, 'error_message': '', 'wall_id': wall.id}
    """
    if check_auth_header_secret():
        resp = add_new_wall()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_wall', methods=['POST', 'GET'])
def get_wall():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'wallData': wall_dict}
    """
    if check_auth_header_secret():
        resp = get_wall_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_wall', methods=['PUT'])
def update_wall():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'wall_id': wall.id}
    """
    if check_auth_header_secret():
        resp = update_wall_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_wall', methods=['DELETE'])
def delete_wall():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'wall_id': wall.id}
    """
    if check_auth_header_secret():
        resp = delete_wall_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Painting  ==================================
@app.route('/add_painting', methods=['POST'])
def add_painting():
    """
    wall_id = fields.Int(required=True)
    name = fields.Str(required=True)
    detail = fields.Str(required=False)
    uuid = fields.Str(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)
    :return {'result_code': 0, 'error_message': '', 'painting_id': painting.id}
    """
    if check_auth_header_secret():
        resp = add_new_painting()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_painting', methods=['POST', 'GET'])
def get_painting():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'paintingData': painting_dict}
    """
    if check_auth_header_secret():
        resp = get_painting_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_painting', methods=['PUT'])
def update_painting():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    detail = fields.Str(required=False)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'painting_id': painting.id}
    """
    if check_auth_header_secret():
        resp = update_painting_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_painting', methods=['DELETE'])
def delete_painting():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'painting_id': painting.id}
    """
    if check_auth_header_secret():
        resp = delete_painting_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Real Size  ==================================
@app.route('/add_real_size', methods=['POST'])
def add_real_size():
    """
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return {'result_code': 0, 'error_message': '', 'real_size_id': real_size.id}
    """
    if check_auth_header_secret():
        resp = add_new_real_size()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_real_size', methods=['POST', 'GET'])
def get_real_size():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'realSizeData': real_size_dict}
    """
    if check_auth_header_secret():
        resp = get_real_size_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_real_size', methods=['PUT'])
def update_real_size():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'real_size_id': real_size.id}
    """
    if check_auth_header_secret():
        resp = update_real_size_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_real_size', methods=['DELETE'])
def delete_real_size():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'real_size_id': real_size.id}
    """
    if check_auth_header_secret():
        resp = delete_real_size_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Pic Size  ==================================
@app.route('/add_pic_size', methods=['POST'])
def add_pic_size():
    """
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return {'result_code': 0, 'error_message': '', 'pic_size_id': pic_size.id}
    """
    if check_auth_header_secret():
        resp = add_new_pic_size()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_pic_size', methods=['POST', 'GET'])
def get_pic_size():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'picSizeData': pic_size_dict}
    """
    if check_auth_header_secret():
        resp = get_pic_size_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_pic_size', methods=['PUT'])
def update_pic_size():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'pic_size_id': pic_size.id}
    """
    if check_auth_header_secret():
        resp = update_pic_size_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_pic_size', methods=['DELETE'])
def delete_pic_size():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: return jsonify({'result_code': 0, 'error_message': '', 'pic_size_id': pic_size.id})
    """
    if check_auth_header_secret():
        resp = delete_pic_size_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Bg Light  ==================================
@app.route('/add_bg_light', methods=['POST'])
def add_bg_light():
    """
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    width = fields.Float(required=True)
    color = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'bg_light_id': bg_light.id}
    """
    if check_auth_header_secret():
        resp = add_new_bg_light()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_bg_light', methods=['POST', 'GET'])
def get_bg_light():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'bgLightData': bg_light_dict}
    """
    if check_auth_header_secret():
        resp = get_bg_light_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_bg_light', methods=['PUT'])
def update_bg_light():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    width = fields.Float(required=True)
    color = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'bg_light_id': bg_light.id}
    """
    if check_auth_header_secret():
        resp = update_bg_light_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_gb_light', methods=['DELETE'])
def delete_gb_light():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'bg_light_id': bg_light.id}
    """
    if check_auth_header_secret():
        resp = delete_bg_light_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Fg Light  ==================================
@app.route('/add_fg_light', methods=['POST'])
def add_fg_light():
    """
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    color = fields.Int(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'fg_light_id': fg_light.id}
    """
    if check_auth_header_secret():
        resp = add_new_fg_light()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_fg_light', methods=['POST', 'GET'])
def get_fg_light():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'fgLightData': fg_light_dict}
    """
    if check_auth_header_secret():
        resp = get_fg_light_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_fg_light', methods=['PUT'])
def update_fg_light():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    color = fields.Int(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'bg_light_id': bg_light.id}
    """
    if check_auth_header_secret():
        resp = update_fg_light_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_fg_light', methods=['DELETE'])
def delete_fg_light():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'fg_light_id': fg_light.id}
    """
    if check_auth_header_secret():
        resp = delete_fg_light_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Icon  ==================================
@app.route('/add_icon', methods=['POST'])
def add_icon():
    """
    uuid = fields.Str(required=True)
    user_id = fields.Int(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'icon_id': icon.id}
    """
    if check_auth_header_secret():
        resp = add_new_icon()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_icon', methods=['POST', 'GET'])
def get_icon():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'iconData': icon_dict})
    """
    if check_auth_header_secret():
        resp = get_icon_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_icon', methods=['PUT'])
def update_icon():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'icon_id': icon.id}
    """
    if check_auth_header_secret():
        resp = update_icon_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_icon', methods=['DELETE'])
def delete_icon():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'icon_id': icon.id}
    """
    if check_auth_header_secret():
        resp = delete_icon_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Texture  ==================================
@app.route('/add_texture', methods=['POST'])
def add_texture():
    """
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'texture_id': texture.id}
    """
    if check_auth_header_secret():
        resp = add_new_texture()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_texture', methods=['POST', 'GET'])
def get_texture():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'textureData': texture_dict}
    """
    if check_auth_header_secret():
        resp = get_texture_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/update_texture', methods=['PUT'])
def update_texture():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    :return: {'result_code': 0, 'error_message': '', 'texture_id': texture.id}
    """
    if check_auth_header_secret():
        resp = update_texture_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/delete_texture', methods=['DELETE'])
def delete_texture():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'texture_id': texture.id}
    """
    if check_auth_header_secret():
        resp = delete_texture_by_id()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   Global Settings  ==================================
@app.route('/save_global_settings', methods=['POST'])
def save_global_settings():
    """
    uuid = fields.Str(required=True)
    floor_texture_index = fields.Int(required=True)
    wall_texture_index = fields.Int(required=True)
    startup_room_index = fields.Int(required=True)
    floor_texture_name = fields.Str(required=True)
    wall_texture_name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '','global_settings_id': globalSettings.id}
    """
    if check_auth_header_secret():
        resp = save_new_global_settings()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_global_settings_by_id', methods=['POST', 'GET'])
def get_global_settings_with_id():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'globalSettingsData': global_settings_dict}
    """
    if check_auth_header_secret():
        resp = get_global_settings_by_id()
        return resp
    else:
        return 'unknown package!!!'


@app.route('/get_global_settings', methods=['POST', 'GET'])
def get_global_settings():
    """
    uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'uuid': String, 'globalSettingsData': global_settings_dict}
    """
    if check_auth_header_secret():
        resp = get_global_settings_data()
        return resp
    else:
        return 'unknown package!!!'


# ==================================   General  ==================================
def add_headers(resp):
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Headers'] = 'Accept, X-Access-Token, X-Application-Name, X-Request-Sent-Time'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def check_auth_header_secret():
    """
    Check if the incoming request's header contains our secretr key
    :return: true if it contains
    """
    return True
    # bearer_header = request.headers.get('Authorization')
    # return 'bearer ' + app.config.get('SECRET_KEY') == bearer_header

# You need to call app.run last, as it blocks execution of anything after it until the server is killed.
# Preferably, use the flask run command instead.
# Ref: https://github.com/pallets/flask/issues/2415
# app.run(debug=True, use_debugger=True, use_reloader=False, passthrough_errors=True)
