from flask import jsonify, json

from app import db
from app.config.constants import ErrorCodes
from app.config.defaults_items_ids import DefaultItemsIds
from app.config.user_status import UserStatus
from app.controllers.schemas import AddNewTextureSchema, GetTextureByIdSchema, UpdateTextureByIdSchema, \
    DeleteTextureByIdSchema, GetDefaultRoomTextureSchema, UpdateDefaultRoomTextureSchema, \
    GetDefaultCeilingTextureSchema, UpdateDefaultCeilingTextureSchema, GetDefaultWallTextureSchema, \
    UpdateDefaultWallTextureSchema
from app.controllers.session_manager import get_user_id
from app.models import Defaults
from app.models import Texture
from app.models import User
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_new_texture_schema = AddNewTextureSchema()
get_texture_by_id_schema = GetTextureByIdSchema()
update_texture_by_id_schema = UpdateTextureByIdSchema()
delete_texture_by_id_schema = DeleteTextureByIdSchema()
get_default_room_texture_schema = GetDefaultRoomTextureSchema()
update_default_room_texture_schema = UpdateDefaultRoomTextureSchema()
get_default_ceiling_texture_schema = GetDefaultCeilingTextureSchema()
update_default_ceiling_texture_schema = UpdateDefaultCeilingTextureSchema()
get_default_wall_texture_schema = GetDefaultWallTextureSchema()
update_default_wall_texture_schema = UpdateDefaultWallTextureSchema()


def generate_texture_created_success_response(texture):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'texture_id': str(texture.id)})


def generate_texture_updated_successfully_response(texture):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'texture_id': str(texture.id)})


def generate_texture_deleted_successfully_response(texture):
    return json.dumps(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'texture_id': str(texture.id)})


def generate_texture_not_found_response(texture_id):
    return json.dumps(
        create_error_response(ErrorCodes.ERROR_CODE_TEXTURE_NOT_FOUND,
                              'texture not found: ' + str(texture_id.item_id)))


def generate_default_value_not_found_response():
    return json.dumps(
        create_error_response(ErrorCodes.ERROR_CODE_DEFAULT_TEXTURE_NOT_FOUND, 'default texture not found'))


def generate_user_not_authorised_response():
    return json.dumps(
        create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_AUTHORIZED, 'User not authorized for this action'))


def generate_user_not_login_response():
    return json.dumps(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_texture_schema)
def add_new_texture(data):
    uuid = data.get('uuid')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        texture = Texture(src=src, width=width, height=height)
        texture.save()
        return generate_texture_created_success_response(texture)
    else:
        return generate_user_not_login_response()


@validate_schema(get_texture_by_id_schema)
def get_texture_by_id(data):
    uuid = data.get('uuid')
    texture_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        texture = db.session.query(Texture).get(texture_id)
        if texture:
            texture_dict = texture.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'textureData': texture_dict})
        else:
            return generate_texture_not_found_response(texture_id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_texture_by_id_schema)
def update_texture_by_id(data):
    uuid = data.get('uuid')
    texture_id = data.get('id')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        texture = db.session.query(Texture).get(texture_id)
        if texture:
            texture.src = src
            texture.width = width
            texture.height = height
            texture.update_texture()
            return generate_texture_updated_successfully_response(texture)
        else:
            return generate_texture_not_found_response(texture_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_texture_by_id_schema)
def delete_texture_by_id(data):
    uuid = data.get('uuid')
    texture_id = data.get('id')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        texture = db.session.query(Texture).get(texture_id)
        if texture:
            texture.delete_texture()
            return generate_texture_deleted_successfully_response(texture)
        else:
            return generate_texture_not_found_response(texture_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_default_room_texture_schema)
def get_default_room_texture(data):
    uuid = data.get('uuid')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        texture_id = db.session.query(Defaults).filter_by(
            item_type=DefaultItemsIds.DEFAULT_ROOM_TEXTURE_ID.value).first()
        if texture_id:
            texture = db.session.query(Texture).get(texture_id.item_id)
            if texture:
                texture_dict = texture.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                     'textureData': texture_dict})
            else:
                return generate_texture_not_found_response(texture_id=texture_id)
        else:
            return generate_default_value_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(update_default_room_texture_schema)
def update_default_room_texture(data):
    uuid = data.get('uuid')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        user = db.session.query(User).filter_by(username=user_id).first()
        if user and user.status == UserStatus.ADMIN_USER.value:
            texture_id = db.session.query(Defaults).filter_by(
                item_type=DefaultItemsIds.DEFAULT_ROOM_TEXTURE_ID.value).first()
            if texture_id:
                texture = db.session.query(Texture).get(texture_id.item_id)
                if texture:
                    texture.src = src
                    texture.width = width
                    texture.height = height
                    texture.update_texture()
                    return generate_texture_updated_successfully_response(texture)
                else:
                    texture = create_texture(DefaultItemsIds.DEFAULT_ROOM_TEXTURE_ID.value, src, width, height)
                    return generate_texture_created_success_response(texture)
            else:
                texture = create_texture(DefaultItemsIds.DEFAULT_ROOM_TEXTURE_ID.value, src, width, height)
                return generate_texture_created_success_response(texture)
        else:
            return generate_user_not_authorised_response()
    else:
        return generate_user_not_login_response()


def create_texture(item_type, src, width, height):
    texture = Texture(src=src, width=width, height=height)
    texture.save()
    default = None
    try:
        default = db.session.query(Defaults).filter_by(item_type=item_type).first()
    except Exception as err:
        print(err)
    if default:
        default.item_id = texture.id
        default.update_default()
    else:
        default = Defaults(item_type=item_type, item_id=texture.id)
        default.save()
    return texture


@validate_schema(get_default_ceiling_texture_schema)
def get_default_ceiling_texture(data):
    uuid = data.get('uuid')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        texture_id = db.session.query(Defaults).filter_by(
            item_type=DefaultItemsIds.DEFAULT_CEILING_TEXTURE_ID.value).first()
        if texture_id:
            texture = db.session.query(Texture).get(texture_id.item_id)
            if texture:
                texture_dict = texture.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                     'textureData': texture_dict})
            else:
                generate_texture_not_found_response(texture_id=texture_id)
        else:
            return generate_default_value_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(update_default_ceiling_texture_schema)
def update_default_ceiling_texture(data):
    uuid = data.get('uuid')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        user = db.session.query(User).filter_by(username=user_id).first()
        if user and user.status == UserStatus.ADMIN_USER.value:
            texture_id = db.session.query(Defaults).filter_by(
                item_type=DefaultItemsIds.DEFAULT_CEILING_TEXTURE_ID.value).first()
            if texture_id:
                texture = db.session.query(Texture).get(texture_id)
                if texture:
                    texture.src = src
                    texture.width = width
                    texture.height = height
                    texture.update_texture()
                    return generate_texture_updated_successfully_response(texture)
                else:
                    texture = create_texture(DefaultItemsIds.DEFAULT_CEILING_TEXTURE_ID.value, src, width, height)
                    return generate_texture_created_success_response(texture)
            else:
                texture = create_texture(DefaultItemsIds.DEFAULT_CEILING_TEXTURE_ID.value, src, width, height)
                return generate_texture_created_success_response(texture)
        else:
            return generate_user_not_authorised_response()
    else:
        return generate_user_not_login_response()


@validate_schema(get_default_wall_texture_schema)
def get_default_wall_texture(data):
    uuid = data.get('uuid')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        texture_id = db.session.query(Defaults).filter_by(
            item_type=DefaultItemsIds.DEFAULT_WALL_TEXTURE_ID.value).first()
        if texture_id:
            texture = db.session.query(Texture).get(texture_id.item_id)
            if texture:
                texture_dict = texture.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                     'textureData': texture_dict})
            else:
                generate_texture_not_found_response(texture_id=texture_id)
        else:
            return generate_default_value_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(update_default_wall_texture_schema)
def update_default_wall_texture(data):
    uuid = data.get('uuid')
    src = data.get('src')
    width = data.get('width')
    height = data.get('height')
    user_id = get_user_id(uuid=uuid)
    if user_id:
        user = db.session.query(User).filter_by(username=user_id).first()
        if user and user.status == UserStatus.ADMIN_USER.value:
            texture_id = db.session.query(Defaults).filter_by(
                item_type=DefaultItemsIds.DEFAULT_WALL_TEXTURE_ID.value).first()
            if texture_id:
                texture = db.session.query(Texture).get(texture_id.item_id)
                if texture:
                    texture.src = src
                    texture.width = width
                    texture.height = height
                    texture.update_texture()
                    return generate_texture_updated_successfully_response(texture)
                else:
                    texture = create_texture(DefaultItemsIds.DEFAULT_WALL_TEXTURE_ID.value, src, width, height)
                    return generate_texture_created_success_response(texture)
            else:
                texture = create_texture(DefaultItemsIds.DEFAULT_WALL_TEXTURE_ID.value, src, width, height)
                return generate_texture_created_success_response(texture)
        else:
            return generate_user_not_authorised_response()
    else:
        return generate_user_not_login_response()
