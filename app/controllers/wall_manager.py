from flask import jsonify, json

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddWallSchema, GetWallByIdSchema, UpdateWallByIdSchema, DeleteWallByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import Wall, Painting
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_wall_schema = AddWallSchema()
get_wall_by_id_schema = GetWallByIdSchema()
update_wall_by_id_schema = UpdateWallByIdSchema()
delete_wall_by_id_schema = DeleteWallByIdSchema()


def generate_user_not_login_response():
    return json.dumps(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


def generate_wall_not_found_response(wall_id):
    return json.dumps(create_error_response(ErrorCodes.ERROR_CODE_WALL_NOT_FOUND, 'Wall not found: ' + wall_id))


def generate_wall_contains_paintings_response(wall_id):
    return json.dumps(create_error_response(ErrorCodes.ERROR_CODE_WALL_CONTAINS_PAINTINGS, 'Wall ' + wall_id + ' contains \
        paintings and cant be removed'))


def generate_wall_updated_successfully_response(wall):
    return json.dumps({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'wall_id': str(wall.id)})


def generate_wall_deleted_successfully_response(wall):
    return json.dumps({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'wall_id': str(wall.id)})


def generate_wall_created_success_response(wall):
    return json.dumps({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'wall_id': str(wall.id)})


@validate_schema(add_wall_schema)
def add_new_wall(data):
    uuid = data.get('uuid')
    name = data.get('name')
    texture_id = data.get('texture_id')
    room_id = data.get('room_id')
    x_pos = data.get('x_pos')
    y_pos = data.get('y_pos')
    z_pos = data.get('z_pos')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        wall = Wall(room_id=room_id, texture_id=texture_id, name=name, x_pos=x_pos, y_pos=y_pos, z_pos=z_pos)
        wall.save()
        return generate_wall_created_success_response(wall)
    else:
        return generate_user_not_login_response()


@validate_schema(get_wall_by_id_schema)
def get_wall_by_id(data):
    uuid = data.get('uuid')
    wall_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        wall = db.session.query(Wall).get(wall_id)
        if wall:
            wall_dict = wall.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'wallData': wall_dict})
        else:
            return generate_wall_not_found_response(wall_id)
    else:
        return generate_user_not_login_response()


# @validate_schema(get_wall_by_id_schema)
# def get_wall_by_id(data):
#     uuid = data.get('uuid')
#     wall_id = data.get('id')
#     user_id = get_user_id(uuid=uuid)
#     if user_id:
#         wall = db.session.query(Wall).get(wall_id).first()
#         if wall:
#             wall_dict = wall.__dict__
#             paintings_dicts = []
#             # Get Paintings
#             paintings = db.session.query(Painting).filter_by(wall_id=wall_id)
#             for a_painting in paintings:
#                 a_painting_dict = a_painting.__dict__
#                 # Get Bg Lights
#                 bg_lights_dicts = []
#                 bg_lights = db.session.query(BgLight).filter_by(painting_id=a_painting.id)
#                 for a_bg_light in bg_lights:
#                     a_bg_light_dict = a_bg_light.__dict__
#                     bg_lights_dicts.append(a_bg_light_dict)
#                 a_painting_dict['gb_lights'] = bg_lights_dicts
#                 # Get Fg Light
#                 fg_lights_dicts = []
#                 fg_lights = db.session.query(FgLight).filter_by(painting_id=a_painting.id)
#                 for a_fg_light in fg_lights:
#                     a_fg_light_dict = a_fg_light.__dict__
#                     fg_lights_dicts.append(a_fg_light_dict)
#                 a_painting_dict['fg_lights'] = fg_lights_dicts
#                 # Get Real Size
#                 real_size_dicts = []
#                 real_sizes = db.session.query(RealSize).filter_by(painting_id=a_painting.id)
#                 for a_real_size in real_sizes:
#                     a_real_size_dict = a_real_size.__dict__
#                     real_size_dicts.append(a_real_size_dict)
#                 a_painting_dict['real_sizes'] = real_size_dicts
#                 # Get Pic Size
#                 pic_size_dicts = []
#                 pic_sizes = db.session.query(PicSize).filter_by(painting_id=a_painting.id)
#                 for a_pic_size in pic_sizes:
#                     a_pic_size_dict = a_pic_size.__dict__
#                     pic_size_dicts.append(a_pic_size_dict)
#                 a_painting_dict['pic_sizes'] = pic_size_dicts
#                 paintings_dicts.append(a_painting_dict)
#             wall_dict['paintings'] = paintings_dicts
#             return jsonify(
#                 {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'wallData': wall_dict})
#         else:
#             return generate_wall_not_found_response(wall_id)
#     else:
#         return generate_user_not_login_response()
#
#
@validate_schema(update_wall_by_id_schema)
def update_wall_by_id(data):
    uuid = data.get('uuid')
    wall_id = data.get('id')
    name = data.get('name')
    texture_id = data.get('texture_id')
    x_pos = data.get('x_pos')
    y_pos = data.get('y_pos')
    z_pos = data.get('z_pos')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        wall = db.session.query(Wall).get(wall_id)
        if wall:
            wall.name = name
            wall.texture_id = texture_id
            wall.x_pos = x_pos
            wall.y_pos = y_pos
            wall.z_pos = z_pos
            wall.update_wall()
            return generate_wall_updated_successfully_response(wall)
        else:
            return generate_wall_not_found_response(wall_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_wall_by_id_schema)
def delete_wall_by_id(data):
    uuid = data.get('uuid')
    wall_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        wall = db.session.query(Wall).get(wall_id)
        if wall:
            paintings = db.session.query(Painting).filter_by(wall_id=wall_id).all()
            if paintings and len(paintings) > 0:
                return generate_wall_contains_paintings_response(wall_id)
            else:
                wall = wall.delete_wall()
                return generate_wall_deleted_successfully_response(wall)
        else:
            return generate_wall_not_found_response(wall_id)
    else:
        return generate_user_not_login_response()
