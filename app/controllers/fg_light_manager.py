from flask import jsonify

from app.config.constants import ErrorCodes
from app.controllers.schemas import AddFgLightSchema, GetFgLightByIdSchema, UpdateFgLightByIdSchema, \
    DeleteFgLightByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import FgLight
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_fg_light_schema = AddFgLightSchema()
get_fg_light_by_id_schema = GetFgLightByIdSchema()
update_fg_light_by_id_schema = UpdateFgLightByIdSchema()
delete_fg_light_by_id_schema = DeleteFgLightByIdSchema()

from app import db


def generate_fg_light_created_success_response(fg_light):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'fg_light_id': fg_light.id})


def generate_fg_light_deleted_successfully_response(fg_light):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'fg_light_id': fg_light.id})


def generate_fg_light_updated_successfully_response(fg_light):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'fg_light_id': fg_light.id})


def generate_fg_light_not_found_response(fg_light_id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_FG_LIGHT_NOT_FOUND, 'Fg Light not found: ' + fg_light_id))


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_fg_light_schema)
def add_new_fg_light(data):
    uuid = data.get('uuid')
    painting_id = data.get('painting_id')
    color = data.get('color')
    x_pos = data.get('x_pos')
    y_pos = data.get('y_pos')
    z_pos = data.get('z_pos')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        fg_light = FgLight(painting_id=painting_id, color=color, x_pos=x_pos, y_pos=y_pos, z_pos=z_pos)
        fg_light.save()
        return generate_fg_light_created_success_response(fg_light)
    else:
        return generate_user_not_login_response()


@validate_schema(get_fg_light_by_id_schema)
def get_fg_light_by_id(data):
    uuid = data.get('uuid')
    fg_light_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        fg_light = db.session.query(FgLight).get(fg_light_id)
        if fg_light:
            fg_light_dict = fg_light.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'fgLightData': fg_light_dict})
        else:
            return generate_fg_light_not_found_response(fg_light_id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_fg_light_by_id_schema)
def update_fg_light_by_id(data):
    uuid = data.get('uuid')
    fg_light_id = data.get('id')
    color = data.get('color')
    x_pos = data.get('x_pos')
    y_pos = data.get('y_pos')
    z_pos = data.get('z_pos')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        fg_light = db.session.query(FgLight).get(fg_light_id)
        if fg_light:
            fg_light.color = color
            fg_light.x_pos = x_pos
            fg_light.y_pos = y_pos
            fg_light.z_pos = z_pos
            fg_light.update_fg_light()
            return generate_fg_light_updated_successfully_response(fg_light)
        else:
            return generate_fg_light_not_found_response(fg_light_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_fg_light_by_id_schema)
def delete_fg_light_by_id(data):
    uuid = data.get('uuid')
    fg_light_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        fg_light = db.session.query(FgLight).get(fg_light_id).first()
        if fg_light:
            fg_light = fg_light.delete_fg_light()
            return generate_fg_light_deleted_successfully_response(fg_light)
        else:
            return generate_fg_light_not_found_response(fg_light_id)
    else:
        return generate_user_not_login_response()
