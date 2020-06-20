import json

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import SaveGlobalSettingsSchema, GetGlobalSettingsByIdSchema, GetGlobalSettingsDataSchema
from app.controllers.session_manager import get_user_id
from app.models import GlobalSettings
from app.utils.AlchemyEncoder import AlchemyEncoder
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

save_global_settings_schema = SaveGlobalSettingsSchema()
get_global_settings_by_id_schema = GetGlobalSettingsByIdSchema()
get_global_settings_data_schema = GetGlobalSettingsDataSchema()


# Ref: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json

def generate_global_settings_created_success_response(global_settings):
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
         'global_settings_id': global_settings.id})


def generate_global_settings_not_found_response():
    msg = create_error_response(ErrorCodes.ERROR_CODE_GLOBAL_SETTINGS_NOT_FOUND, 'global settings not found')
    return jsonify(msg)


def generate_global_settings_not_found_response_id(s_id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_GLOBAL_SETTINGS_NOT_FOUND, 'global settings not found : ' + s_id))


def generate_user_not_login_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(save_global_settings_schema)
def save_new_global_settings(data):
    user_uuid = data.get('uuid')
    floor_texture_index = data.get('floor_texture_index')
    wall_texture_index = data.get('wall_texture_index')
    startup_room_index = data.get('startup_room_index')
    floor_texture_name = data.get('floor_texture_name')
    wall_texture_name = data.get('wall_texture_name')
    user_id = get_user_id(uuid=user_uuid)
    if user_id:
        global_settings_list = db.session.query(GlobalSettings).all()
        if global_settings_list and len(global_settings_list) > 0:
            global_settings_item = global_settings_list[0]
            global_settings_item.floor_texture_index = floor_texture_index
            global_settings_item.wall_texture_index = wall_texture_index
            global_settings_item.startup_room_index = startup_room_index
            global_settings_item.floor_texture_name = floor_texture_name
            global_settings_item.wall_texture_name = wall_texture_name
            global_settings_item.update_global_settings()
            return generate_global_settings_created_success_response(global_settings_item)
        else:
            global_settings = GlobalSettings(floor_texture_index=floor_texture_index,
                                             wall_texture_index=wall_texture_index,
                                             startup_room_index=startup_room_index,
                                             floor_texture_name=floor_texture_name,
                                             wall_texture_name=wall_texture_name)
            global_settings.save()
            return generate_global_settings_created_success_response(global_settings)
    else:
        return generate_user_not_login_response()


@validate_schema(get_global_settings_by_id_schema)
def get_global_settings_by_id(data):
    user_uuid = data.get('uuid')
    id = data.get('id')
    user_id = get_user_id(uuid=user_uuid)
    if user_id:
        global_settings = db.session.query(GlobalSettings).get(id)
        if global_settings:
            global_settings_dict = global_settings.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                 'globalSettingsData': global_settings_dict})
        else:
            return generate_global_settings_not_found_response_id(id)
    else:
        return generate_user_not_login_response()



@validate_schema(get_global_settings_data_schema)
def get_global_settings_data(data):
    user_uuid = data.get('uuid')
    user_id = get_user_id(uuid=user_uuid)
    if user_id:
        global_settings_list = db.session.query(GlobalSettings).all()
        if global_settings_list and len(global_settings_list) > 0:
            global_settings_item = global_settings_list[0]
            global_settings_json = json.dumps(global_settings_item, cls=AlchemyEncoder)
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                 'globalSettingsData': global_settings_json})
        else:
            return generate_global_settings_not_found_response()
    else:
        return generate_user_not_login_response()


# @validate_schema(get_global_settings_data_schema)
# def get_global_settings_data(data):
#     user_uuid = data.get('uuid')
#     # user_id = get_user_id(uuid=user_uuid)
#     # if user_id:
#     global_settings_list = db.session.query(GlobalSettings).all()
#     if global_settings_list and len(global_settings_list) > 0:
#         global_settings_item = global_settings_list[0]
#         global_settings_json = json.dumps(global_settings_item, cls=AlchemyEncoder)
#         dsfsdf
#         return jsonify(
#             {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
#              'globalSettingsData': global_settings_json})
#     else:
#         return generate_global_settings_not_found_response()
# # else:
# #     return generate_user_not_login_response()
