from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddBgLightSchema, GetBgLightByIdSchema, UpdateBgLightByIdSchema, \
    DeleteBgLightByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import BgLight
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_bg_light_schema = AddBgLightSchema()
get_bg_light_by_id_schema = GetBgLightByIdSchema()
update_bg_light_by_id_schema = UpdateBgLightByIdSchema()
delete_bg_light_by_id_schema = DeleteBgLightByIdSchema()


def generate_bg_light_created_success_response(bg_light):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'bg_light_id': bg_light.id})


def generate_bg_light_deleted_successfully_response(bg_light):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'bg_light_id': bg_light.id})


def generate_bg_light_updated_successfully_response(bg_light):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'bg_light_id': bg_light.id})


def generate_bg_light_not_found_response(bg_light_id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_BG_LIGHT_NOT_FOUND, 'Bg Light not found: ' + bg_light_id))


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_bg_light_schema)
def add_new_bg_light(data):
    uuid = data.get('uuid')
    painting_id = data.get('painting_id')
    width = data.get('width')
    color = data.get('color')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        bg_light = BgLight(painting_id=painting_id, width=width, color=color)
        bg_light.save()
        return generate_bg_light_created_success_response(bg_light)
    else:
        return generate_user_not_login_response()


@validate_schema(get_bg_light_by_id_schema)
def get_bg_light_by_id(data):
    uuid = data.get('uuid')
    bg_light_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        bg_light = db.session.query(BgLight).get(bg_light_id)
        if bg_light:
            bg_light_dict = bg_light.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'bgLightData': bg_light_dict})
        else:
            return generate_bg_light_not_found_response(bg_light_id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_bg_light_by_id_schema)
def update_bg_light_by_id(data):
    uuid = data.get('uuid')
    bg_light_id = data.get('id')
    width = data.get('width')
    color = data.get('color')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        bg_light = db.session.query(BgLight).get(bg_light_id)
        if bg_light:
            bg_light.width = width
            bg_light.color = color
            bg_light.update_bg_light()
            return generate_bg_light_updated_successfully_response(bg_light)
        else:
            return generate_bg_light_not_found_response(bg_light_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_bg_light_by_id_schema)
def delete_bg_light_by_id(data):
    uuid = data.get('uuid')
    bg_light_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        bg_light = db.session.query(BgLight).get(bg_light_id).first()
        if bg_light:
            bg_light = bg_light.delete_bg_light()
            return generate_bg_light_deleted_successfully_response(bg_light)
        else:
            return generate_bg_light_not_found_response(bg_light_id)
    else:
        return generate_user_not_login_response()
