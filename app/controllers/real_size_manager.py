from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddRealSizeSchema, GetRealSizeByIdSchema, UpdateRealSizeByIdSchema, \
    DeleteRealSizeByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import RealSize
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_real_size_schema = AddRealSizeSchema()
get_real_size_by_id_schema = GetRealSizeByIdSchema()
update_real_size_by_id_schema = UpdateRealSizeByIdSchema()
delete_real_size_by_id_schema = DeleteRealSizeByIdSchema()


def generate_real_size_created_success_response(real_size):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'real_size_id': real_size.id})


def generate_real_size_updated_successfully_response(real_size):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'real_size_id': real_size.id})


def generate_real_size_deleted_successfully_response(real_size):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'real_size_id': real_size.id})


def generate_real_size_not_found_response(real_size_id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_REAL_SIZE_NOT_FOUND, 'Real Size not found: ' + real_size_id))


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_real_size_schema)
def add_new_real_size(data):
    uuid = data.get('uuid')
    painting_id = data.get('painting_id')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        real_size = RealSize(painting_id=painting_id, width=width, height=height)
        real_size.save()
        return generate_real_size_created_success_response(real_size)
    else:
        return generate_user_not_login_response()


@validate_schema(get_real_size_by_id_schema)
def get_real_size_by_id(data):
    real_size_id = data.get('id')
    uuid = data.get('uuid')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        real_size = db.session.query(RealSize).get(real_size_id).first()
        if real_size:
            real_size_dict = real_size.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                 'realSizeData': real_size_dict})
        else:
            return generate_real_size_not_found_response(real_size_id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_real_size_by_id_schema)
def update_real_size_by_id(data):
    real_size_id = data.get('id')
    uuid = data.get('uuid')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        real_size = db.session.query(RealSize).get(real_size_id).first()
        if real_size:
            real_size.width = width
            real_size.height = height
            real_size = real_size.update_real_size()
            return generate_real_size_updated_successfully_response(real_size)
        else:
            return generate_real_size_not_found_response(real_size_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_real_size_by_id_schema)
def delete_real_size_by_id(data):
    real_size_id = data.get('id')
    uuid = data.get('uuid')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        real_size = db.session.query(RealSize).get(real_size_id).first()
        if real_size:
            real_size = real_size.delete_real_size()
            return generate_real_size_deleted_successfully_response(real_size)
        else:
            return generate_real_size_not_found_response(real_size_id)
    else:
        return generate_user_not_login_response()
