import requests
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.config.user_status import UserStatus
from app.controllers.schemas import LoginSchema, RegistrationSchema, GetUserIdRemotelySchema
from app.models import User, Session
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.utils.uuid_utils import check_hash_password, generate_uuid, get_hash_password

login_schema = LoginSchema()
registration_schema = RegistrationSchema()
get_user_id_remotely_schema = GetUserIdRemotelySchema()


def generate_login_success_response(temp_uuid):
    try:
        return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'uuid': temp_uuid})
    except Exception as ex:
        print(ex)


def generate_login_failed_response():
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_LOGIN_FAILED, 'Username and Password not found'))


def generate_username_taken_response(username):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_USERNAME_ALREADY_TAKEN, 'Username already taken: ' + username))


def generate_registration_success_response(temp_uuid):
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'uuid': temp_uuid})


def generate_registration_failed_response(exe):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_REGISTRATION_FAILED, 'User registration failed ' + str(exe)))


@validate_schema(get_user_id_remotely_schema)
def get_user_id_remotely(data):
    key = data.get('key')
    url = 'https://veryimportantlot.com/gallery3d/api/auth?key=' + key
    response = requests.get(url)
    user_id = response.text
    if user_id and user_id != '0':
        temp_uuid = generate_uuid()
        session_old = db.session.query(Session).filter_by(email=user_id)
        if session_old:
            session_old.delete()
        session = Session(user_id, temp_uuid)
        if session:
            session.save()
        return generate_login_success_response(temp_uuid)
    else:
        return generate_login_failed_response()


@validate_schema(login_schema)
def user_login(data):
    username = data.get('username')
    password = data.get('password')
    user = None
    try:
        user = db.session.query(User).filter_by(username=username).first()
    except Exception as ex:
        print(ex)
    if user and check_hash_password(user.hash_pwd, user.salt, password) and user.status == UserStatus.ADMIN_USER.value:
        temp_uuid = generate_uuid()
        session_old = db.session.query(Session).filter_by(email=username)
        if session_old:
            session_old.delete()
        session = Session(user.username, temp_uuid)
        if session:
            session.save()
        return generate_login_success_response(temp_uuid)
    else:
        return generate_login_failed_response()


# def user_login(data):
#     username = data.get('username')
#     password = data.get('password')
#     try:
#         user = db.session.query(User).filter_by(username=username).first()
#     except Exception as ex:
#         print(ex)
#     if user and check_hash_password(user.hash_pwd, user.salt, password) and user.status == UserStatus.ADMIN_USER.value:
#         temp_uuid = generate_uuid()
#         session_old = db.session.query(Session).filter_by(email=username)
#         if session_old:
#             session_old.delete()
#         session = Session(user.username, temp_uuid)
#         if session:
#             session.save()
#         return generate_login_success_response(temp_uuid)
#     else:
#         return generate_login_failed_response()


@validate_schema(registration_schema)
def user_register(data):
    try:
        username = data.get('username')
        password = data.get('password')
        language = data.get('language')
        status = data.get('status')
        if is_user_exist(username):
            return generate_username_taken_response(username)
        salt = generate_uuid()
        hash_pwd = get_hash_password(salt, password)
        user = User(username=username, hash_pwd=hash_pwd, salt=salt, language=language, status=status)
        if user:
            temp_uuid = generate_uuid()
            session = Session(username=user.username, uuid=temp_uuid)
            user.save(session)
            return generate_registration_success_response(temp_uuid)
        else:
            raise Exception('Failed to create user')
    except Exception as exe:
        print('user user registration failed')
        if hasattr(exe, 'message'):
            print(exe.message)
        else:
            print(exe)
        return generate_registration_failed_response(exe)


def admin_user_register(data):
    try:
        username = data.get('username')
        password = data.get('password')
        language = data.get('language')
        status = data.get('status')
        salt = generate_uuid()
        hash_pwd = get_hash_password(salt, password)
        user = User(username=username, hash_pwd=hash_pwd, salt=salt, language=language, status=status)
        if user:
            user.save_admin()
        else:
            raise Exception('Failed to create user')
    except Exception as exe:
        print('user user registration failed')
        if hasattr(exe, 'message'):
            print(exe.message)
        else:
            print(exe)
        return generate_registration_failed_response(exe)


def is_admin_exist():
    try:
        user = db.session.query(User).filter_by(username='AdminApp').first()
        if user:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False


def is_user_exist(user_name):
    try:
        user = db.session.query(User).filter_by(username=user_name).first()
        if user:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False
