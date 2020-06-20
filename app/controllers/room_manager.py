from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddRoomSchema, GetRoomByIdSchema, UpdateRoomByIdSchema, DeleteRoomByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import Room, Wall
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_room_schema = AddRoomSchema()
get_room_by_id_schema = GetRoomByIdSchema()
update_room_by_id_schema = UpdateRoomByIdSchema()
delete_room_by_id_schema = DeleteRoomByIdSchema()


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


def generate_room_not_found_response(id):
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ROOM_NOT_FOUND, 'Room not found: ' + id))


def generate_room_contains_walls_response(room_id):
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ROOM_CONTAINS_WALLS, 'Room ' + room_id + ' contains \
    walls and cant be removed'))


def generate_room_updated_successfully_response(room):
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'room_id': room.id})


def generate_room_created_success_response(room):
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'room_id': room.id})


def generate_room_deleted_successfully_response(room):
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'room_id': room.id})


@validate_schema(add_room_schema)
def add_new_room(data):
    uuid = data.get('uuid')
    name = data.get('name')
    texture_id = data.get('texture_id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        room = Room(user_id=user_id, texture_id=texture_id, name=name)
        room.save()
        return generate_room_created_success_response(room)
    else:
        return generate_user_not_login_response()


# @validate_schema(get_room_by_id_schema)
# def get_room_by_id(data):
#     uuid = data.get('uuid')
#     id = data.get('id')
#     session = db.session.query(Session).filter(uuid=uuid).first()
#     if session:
#         # Get Room
#         room = db.session.query(Room).get(id).first()
#         if room:
#             room_dict = room.__dict__
#             walls_dicts = []
#             # Get Walls
#             walls = db.session.query(Wall).filter_by(room_id=id)
#             if walls and len(walls) > 0:
#                 for a_wall in walls:
#                     a_wall_dict = a_wall.__dict__
#                     paintings_dicts = []
#                     # Get Paintings
#                     paintings = db.session.query(Painting).filter_by(wall_id=a_wall.id)
#                     for a_painting in paintings:
#                         a_painting_dict = a_painting.__dict__
#                         # Get Bg Lights
#                         bg_lights_dicts = []
#                         bg_lights = db.session.query(BgLight).filter_by(painting_id=a_painting.id)
#                         for a_bg_light in bg_lights:
#                             a_bg_light_dict = a_bg_light.__dict__
#                             bg_lights_dicts.append(a_bg_light_dict)
#                         a_painting_dict['gb_lights'] = bg_lights_dicts
#                         # Get Fg Light
#                         fg_lights_dicts = []
#                         fg_lights = db.session.query(FgLight).filter_by(painting_id=a_painting.id)
#                         for a_fg_light in fg_lights:
#                             a_fg_light_dict = a_fg_light.__dict__
#                             fg_lights_dicts.append(a_fg_light_dict)
#                         a_painting_dict['fg_lights'] = fg_lights_dicts
#                         # Get Real Size
#                         real_size_dicts = []
#                         real_sizes = db.session.query(RealSize).filter_by(painting_id=a_painting.id)
#                         for a_real_size in real_sizes:
#                             a_real_size_dict = a_real_size.__dict__
#                             real_size_dicts.append(a_real_size_dict)
#                         a_painting_dict['real_sizes'] = real_size_dicts
#                         # Get Pic Size
#                         pic_size_dicts = []
#                         pic_sizes = db.session.query(PicSize).filter_by(painting_id=a_painting.id)
#                         for a_pic_size in pic_sizes:
#                             a_pic_size_dict = a_pic_size.__dict__
#                             pic_size_dicts.append(a_pic_size_dict)
#                         a_painting_dict['pic_sizes'] = pic_size_dicts
#                         paintings_dicts.append(a_painting_dict)
#                     a_wall_dict['paintings'] = paintings_dicts
#                 walls_dicts.append(a_wall_dict)
#             room_dict['walls'] = walls_dicts
#             return jsonify(
#                 {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'roomData': room_dict})
#         else:
#             return generate_room_not_found_response(id)
#     else:
#         return generate_user_not_login_response()


@validate_schema(get_room_by_id_schema)
def get_room_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        # Get Room
        room = db.session.query(Room).get(id).first()
        if room:
            room_dict = room.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'roomData': room_dict})
        else:
            return generate_room_not_found_response(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_room_by_id_schema)
def update_room_by_id(data):
    uuid = data.get('uuid')
    room_id = data.get('id')
    name = data.get('name')
    texture_id = data.get('texture_id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        room = db.session.query(Room).get(room_id).first()
        if room:
            room.name = name
            room.texture_id = texture_id
            room = room.update_room()
            return generate_room_updated_successfully_response(room)
        else:
            generate_room_not_found_response(room_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_room_by_id_schema)
def delete_room_by_id(data):
    uuid = data.get('uuid')
    room_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        room = db.session.query(Room).get(room_id).first()
        if room:
            walls = db.session.query(Wall).filter_by(room_id=room_id)
            if walls and len(walls) > 0:
                return generate_room_contains_walls_response(room_id)
            else:
                room = room.delete_room()
                return generate_room_deleted_successfully_response(room)
        else:
            generate_room_not_found_response(room_id)
    else:
        return generate_user_not_login_response()
