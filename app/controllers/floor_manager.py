from flask import jsonify, json

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddFloorSchema, GetFloorByIdSchema, UpdateFloorByIdSchema, DeleteFloorByIdSchema
from app.controllers.session_manager import get_user_id
from app.models import Floor
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_floor_schema = AddFloorSchema()
get_floor_by_id_schema = GetFloorByIdSchema()
update_floor_by_id_schema = UpdateFloorByIdSchema()
delete_floor_by_id_schema = DeleteFloorByIdSchema()


def generate_floor_deleted_successfully_response(floor):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'floor_id': str(floor.id)})


def generate_floor_name_already_exist_response(name):
    return json.dumps(
        create_error_response(ErrorCodes.ERROR_CODE_FLOOR_ALREADY_EXIST, 'Floor ' + name + ' already exist'))


def generate_floor_not_found_response(id):
    return json.dumps(create_error_response(ErrorCodes.ERROR_CODE_FLOOR_NOT_FOUND, 'Floor not found: ' + str(id)))


def generate_user_not_login_response():
    return json.dumps(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


def generate_floor_created_success_response(floor):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'floor_id': str(floor.id)})


def generate_floor_updated_successfully_response(floor):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'floor_id': str(floor.id)})


@validate_schema(add_floor_schema)
def add_new_floor(data):
    name = data.get('name')
    uuid = data.get('uuid')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor = Floor(user_id=user_id, name=name)
        try:
            floor.save()
        except Exception as err:
            return generate_floor_name_already_exist_response(name)
        return generate_floor_created_success_response(floor)
    else:
        return generate_user_not_login_response()


@validate_schema(get_floor_by_id_schema)
def get_floor_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor = db.session.query(Floor).get(id)
        if floor:
            floor_dict = floor.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'floorData': floor_dict})
        else:
            return generate_floor_not_found_response(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_floor_by_id_schema)
def update_floor_by_id(data):
    name = data.get('name')
    uuid = data.get('uuid')
    id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor = db.session.query(Floor).get(id)
        if floor:
            floor.name = name
            floor = floor.update_floor()
            floor_dict = floor.to_dict
            floor_dict = floor.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'floorData': floor_dict})
            # try:
            #     floor.save()
            # except Exception as err:
            #     return generate_floor_name_already_exist_response(name=name)
            # return generate_floor_updated_successfully_response(floor)
        else:
            return generate_floor_not_found_response(id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_floor_by_id_schema)
def delete_floor_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor = db.session.query(Floor).get(id)
        if floor:
            floor.delete_floor()
            return generate_floor_deleted_successfully_response(floor)
        else:
            return generate_floor_not_found_response(id)
    else:
        return generate_user_not_login_response()
