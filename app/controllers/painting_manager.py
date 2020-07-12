from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddPaintingSchema, GetPaintingByIdSchema, UpdatePaintingByIdSchema, \
    DeletePaintingByIdShema
from app.controllers.session_manager import get_user_id
from app.models import Painting, BgLight, FgLight, RealSize, PicSize
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_painting_schema = AddPaintingSchema()
get_painting_by_id_schema = GetPaintingByIdSchema()
update_painting_by_id_schema = UpdatePaintingByIdSchema()
delete_painting_by_id_schema = DeletePaintingByIdShema()


def generate_painting_created_success_response(painting):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'painting_id': painting.id})


def generate_painting_not_found_response(painting_id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_PAINTING_NOT_FOUND, 'Painting not found: ' + painting_id))


def generate_painting_contains_pic_sizes_response(painting_id):
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_PAINTING_CONTAINS_PIC_SIZES, 'Painting ' + painting_id + ' contains \
                    Pic Sizes and cant be removed'))


def generate_painting_contains_real_sizes_response(painting_id):
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_PAINTING_CONTAINS_REAL_SIZES, 'Painting ' + painting_id + ' contains \
                Real Sizes and cant be removed'))


def generate_painting_contains_fg_lights_response(painting_id):
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_PAINTING_CONTAINS_FG_LIGHTS, 'Painting ' + painting_id + ' contains \
            Fg Lights and cant be removed'))


def generate_painting_contains_bg_lights_response(painting_id):
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_PAINTING_CONTAINS_BG_LIGHTS, 'Painting ' + painting_id + ' contains \
        Bg Lights and cant be removed'))


def generate_painting_updated_successfully_response(painting):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'painting_id': painting.id})


def generate_painting_deleted_successfully_response(painting):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'painting_id': painting.id})


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_painting_schema)
def add_new_painting(data):
    uuid = data.get('uuid')
    name = data.get('name')
    detail = data.get('detail')
    wall_id = data.get('wall_id')
    x_pos = data.get('x_pos')
    y_pos = data.get('y_pos')
    z_pos = data.get('z_pos')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        painting = Painting(wall_id=wall_id, name=name, detail=detail, x_pos=x_pos, y_pos=y_pos, z_pos=z_pos)
        painting.save()
        return generate_painting_created_success_response(painting)
    else:
        return generate_user_not_login_response()


# @validate_schema(get_painting_by_id_schema)
# def get_painting_by_id(data):
#     uuid = data.get('uuid')
#     painting_id = data.get('id')
#     user_id = get_user_id(uuid=uuid)
#     if user_id:
#         painting = db.session.query(Painting).get(painting_id).first()
#         if painting:
#             painting_dict = painting.to_dict()
#             bg_lights_dicts = []
#
#             # Get Bg Light
#             bg_lights = db.session.query(BgLight).filter_by(painting_id=painting.id).first()
#             for a_bg_light in bg_lights:
#                 a_bg_light_dict = a_bg_light.__dict__
#                 bg_lights_dicts.append(a_bg_light_dict)
#             painting_dict['gb_lights'] = bg_lights_dicts
#
#             # Get Fg Light
#             fg_lights_dicts = []
#             fg_lights = db.session.query(FgLight).filter_by(painting_id=painting.id).first()
#             for a_fg_light in fg_lights:
#                 a_fg_light_dict = a_fg_light.__dict__
#                 fg_lights_dicts.append(a_fg_light_dict)
#             painting_dict['fg_lights'] = fg_lights_dicts
#
#             # Get Real Size
#             real_size_dicts = []
#             real_sizes = db.session.query(RealSize).filter(painting_id=painting.id).first()
#             for a_real_size in real_sizes:
#                 a_real_size_dict = a_real_size.__dict__
#                 real_size_dicts.append(a_real_size_dict)
#             painting_dict['real_sizes'] = real_size_dicts
#
#             # Get Pic Size
#             pic_size_dicts = []
#             pic_sizes = db.session.query(PicSize).filter_by(painting_id=painting.id)
#             for a_pic_size in pic_sizes:
#                 a_pic_size_dict = a_pic_size.__dict__
#                 pic_size_dicts.append(a_pic_size_dict)
#
#             painting_dict['pic_sizes'] = pic_size_dicts
#             return jsonify(
#                 {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
#                  'paintingData': painting_dict})
#         else:
#             return generate_painting_not_found_response(painting_id)
#     else:
#         return generate_user_not_login_response()


@validate_schema(get_painting_by_id_schema)
def get_painting_by_id(data):
    uuid = data.get('uuid')
    painting_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        painting = db.session.query(Painting).get(painting_id)
        if painting:
            painting_dict = painting.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                 'paintingData': painting_dict})
        else:
            return generate_painting_not_found_response(painting_id)
    else:
        return generate_user_not_login_response()



@validate_schema(update_painting_by_id_schema)
def update_painting_by_id(data):
    uuid = data.get('uuid')
    painting_id = data.get('id')
    name = data.get('name')
    detail = data.get('detail')
    x_pos = data.get('x_pos')
    y_pos = data.get('y_pos')
    z_pos = data.get('z_pos')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        painting = db.session.query(Painting).get(painting_id)
        if painting:
            painting.name = name
            painting.detail = detail
            painting.x_pos = x_pos
            painting.y_pos = y_pos
            painting.z_pos = z_pos
            painting.update_painting()
            return generate_painting_updated_successfully_response(painting)
        else:
            return generate_painting_not_found_response(painting_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_painting_by_id_schema)
def delete_painting_by_id(data):
    uuid = data.get('uuid')
    painting_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        painting = db.session.query(Painting).get(painting_id).first()
        if painting:
            bg_lights = db.session.query(BgLight).filter_by(painting_id=painting.id)
            fg_lights = db.session.query(FgLight).filter_by(painting_id=painting.id)
            real_sizes = db.session.query(RealSize).filter_by(painting_id=painting.id)
            pic_sizes = db.session.query(PicSize).filter_by(painting_id=painting.id)
            if bg_lights and len(bg_lights) > 0:
                return generate_painting_contains_bg_lights_response(painting_id)
            elif fg_lights and len(fg_lights) > 0:
                return generate_painting_contains_fg_lights_response(painting_id)
            elif real_sizes and len(real_sizes) > 0:
                return generate_painting_contains_real_sizes_response(painting_id)
            elif pic_sizes and len(pic_sizes) > 0:
                return generate_painting_contains_pic_sizes_response(painting_id)
            else:
                painting = painting.delete_painting()
                return generate_painting_deleted_successfully_response(painting)
        else:
            return generate_painting_not_found_response(painting_id)
    else:
        return generate_user_not_login_response()
