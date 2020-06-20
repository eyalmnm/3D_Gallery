from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddPicSizeSchema, GetPicSizeByIdSchema, UpdatePicSizeByIdSchema, \
    DeletePicSizeByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import PicSize
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_pic_size_schema = AddPicSizeSchema()
get_pic_size_by_id_schema = GetPicSizeByIdSchema()
update_pic_size_by_id_schema = UpdatePicSizeByIdSchema()
delete_pic_size_by_id_schema = DeletePicSizeByIdSchema()


def generate_pic_size_created_success_response(pic_size):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'pic_size_id': pic_size.id})


def generate_pic_size_updated_successfully_response(pic_size):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'pic_size_id': pic_size.id})


def generate_pic_size_deleted_successfully_response(pic_size):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'pic_size_id': pic_size.id})


def generate_pic_size_not_found_response(pic_size_id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_PIC_SIZE_NOT_FOUND, 'Pic Size not found: ' + pic_size_id))


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_pic_size_schema)
def add_new_pic_size(data):
    uuid = data.get('uuid')
    painting_id = data.get('painting_id')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        pic_size = PicSize(painting_id=painting_id, width=width, height=height)
        pic_size.save()
        return generate_pic_size_created_success_response(pic_size)
    else:
        return generate_user_not_login_response()


@validate_schema(get_pic_size_by_id_schema)
def get_pic_size_by_id(data):
    uuid = data.get('uuid')
    pic_size_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        pic_size = db.session.query(PicSize).get(pic_size_id).first()
        if pic_size:
            pic_size_dict = pic_size.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'picSizeData': pic_size_dict})
        else:
            return generate_pic_size_not_found_response(pic_size_id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_pic_size_by_id_schema)
def update_pic_size_by_id(data):
    uuid = data.get('uuid')
    pic_size_id = data.get('id')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        pic_size = db.session.query(PicSize).get(pic_size_id).first()
        if pic_size:
            pic_size.width = width
            pic_size.height = height
            pic_size = pic_size.update_pic_size()
            return generate_pic_size_updated_successfully_response(pic_size)
        else:
            return generate_pic_size_not_found_response(pic_size_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_pic_size_by_id_schema)
def delete_pic_size_by_id(data):
    uuid = data.get('uuid')
    pic_size_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        pic_size = db.session.query(PicSize).get(pic_size_id).first()
        if pic_size:
            pic_size = pic_size.delete_pic_size()
            return generate_pic_size_deleted_successfully_response(pic_size)
        else:
            return generate_pic_size_not_found_response(pic_size_id)
    else:
        return generate_user_not_login_response()
