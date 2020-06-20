from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddNewIconSchema, GetIconByIdSchema, UpdateIconByIdSchema, DeleteIconByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import Icon
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_new_icon_schema = AddNewIconSchema()
get_icon_by_id_schema = GetIconByIdSchema()
update_icon_by_id_schema = UpdateIconByIdSchema()
delete_icon_by_id_schema = DeleteIconByIdSchema()


def generate_icon_created_success_response(icon):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'icon_id': icon.id})


def generate_icon_updated_successfully_response(icon):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'icon_id': icon.id})


def generate_icon_deleted_successfully_response(icon):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'icon_id': icon.id})


def generate_icon_not_found_response(icon_id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_ICON_NOT_FOUND, 'icon not found: ' + icon_id))


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_icon_schema)
def add_new_icon(data):
    uuid = data.get('uuid')
    user_id = data.get('user_id')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        icon = Icon(user_id=user_id, src=src, width=width, height=height)
        icon = icon.save()
        return generate_icon_created_success_response(icon)
    else:
        return generate_user_not_login_response()


@validate_schema(get_icon_by_id_schema)
def get_icon_by_id(data):
    uuid = data.get('uuid')
    icon_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        icon = db.session.query(Icon).get(icon_id)
        if icon:
            icon_dict = icon.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'iconData': icon_dict})
        else:
            return generate_icon_not_found_response(icon_id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_icon_by_id_schema)
def update_icon_by_id(data):
    uuid = data.get('uuid')
    icon_id = data.get('id')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        icon = db.session.query(Icon).get(icon_id)
        if icon:
            icon.src = src
            icon.width = width
            icon.height = height
            icon = icon.update_icon()
            return generate_icon_updated_successfully_response(icon)
        else:
            return generate_icon_not_found_response(icon_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_icon_by_id_schema)
def delete_icon_by_id(data):
    uuid = data.get('uuid')
    icon_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        icon = db.session.query(Icon).get(icon_id)
        if icon:
            icon.delete_icon()
            return generate_icon_deleted_successfully_response(icon)
        else:
            return generate_icon_not_found_response(icon_id)
    else:
        return generate_user_not_login_response()
