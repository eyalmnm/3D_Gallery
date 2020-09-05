from flask import jsonify, json

from app import db
from app.config.constants import ErrorCodes
from app.controllers.session_manager import get_user_id
from app.utils.exception_util import create_error_response
from app.models import FloorTexture
from app.utils.schema_utils import validate_schema
from app.controllers.schemas import AddNewFloorTextureSchema, GetFloorTextureByIdSchema, GetFloorTextureByFloorIdSchema, \
    UpdateFloorTextureByIdSchema

# Ref: https://stackoverflow.com/questions/3070242/reduce-list-of-python-objects-to-dict-of-object-id-object

add_new_floor_texture_schema = AddNewFloorTextureSchema()
get_floor_texture_by_id_schema = GetFloorTextureByIdSchema()
get_floor_texture_by_floor_id_schema = GetFloorTextureByFloorIdSchema()
update_floor_texture_by_id_schema = UpdateFloorTextureByIdSchema()


def generate_texture_created_success_response(texture):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'texture_id': str(texture.id)})


def generate_texture_updated_successfully_response(texture):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'texture_id': str(texture.id)})


def generate_texture_not_found_response(texture_id):
    return json.dumps(
        create_error_response(ErrorCodes.ERROR_CODE_TEXTURE_NOT_FOUND,
                              'texture not found: ' + str(texture_id.item_id)))


def generate_user_not_login_response():
    return json.dumps(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_floor_texture_schema)
def add_new_floor_texture(data):
    uuid = data.get('uuid')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    floor_id = data.get('floor_id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor_texture = FloorTexture(src, floor_id, width, height)
        floor_texture.save()
        return generate_texture_created_success_response(floor_texture)
    else:
        return generate_user_not_login_response()


@validate_schema(get_floor_texture_by_id_schema)
def get_floor_texture_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor_texture = db.session.query(FloorTexture).get(id)
        if floor_texture:
            floor_texture_dict = floor_texture.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                 'textureData': floor_texture_dict})
        else:
            return generate_texture_not_found_response(id)
    else:
        return generate_user_not_login_response()


# Ref: https://stackoverflow.com/questions/3070242/reduce-list-of-python-objects-to-dict-of-object-id-object
@validate_schema(get_floor_texture_by_floor_id_schema)
def get_floor_texture_by_floor_id(data):
    uuid = data.get('uuid')
    floor_id = data.get('floor_id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor_textures = db.session.query(FloorTexture).filter_by(floor_id=floor_id).all()
        if floor_textures and len(floor_textures) > 0:
            textures_dict = {f_text.id: f_text for f_text in floor_textures}
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                 'texturesData': textures_dict})
        else:
            return generate_texture_not_found_response(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_floor_texture_by_id_schema)
def update_floor_texture_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    floor_id = data.get('floor_id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        floor_texture = db.session.query(FloorTexture).get(id)
        if floor_texture:
            floor_texture.src = src
            floor_texture.width = width
            floor_texture.height = height
            floor_texture.floor_id = floor_id
            floor_texture.update_texture()
            return generate_texture_updated_successfully_response(floor_texture)
        else:
            return generate_texture_not_found_response(id)
    else:
        return generate_user_not_login_response()
