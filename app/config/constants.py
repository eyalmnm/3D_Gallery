from enum import Enum


class ErrorCodes(Enum):
    ERROR_CODE_SUCCESS = 0
    VALIDATE_INPUT_SCHEMA_FAILED = 10
    ERROR_CODE_USER_NOT_AUTHORIZED = 20

    # Login Error codes (100 - 199)
    ERROR_CODE_LOGIN_FAILED = 100
    ERROR_CODE_USER_NOT_LOGGED_IN = 101

    # Login Error codes (200 - 299)
    ERROR_CODE_REGISTRATION_FAILED = 200
    ERROR_CODE_USERNAME_ALREADY_TAKEN = 201

    # Room Error Codes (300 - 399)
    ERROR_CODE_ROOM_NOT_FOUND = 300
    ERROR_CODE_ROOM_CONTAINS_WALLS = 301
    ERROR_CODE_ROOM_ALREADY_EXIST = 302

    # Wall Error Codes (400 - 499)
    ERROR_CODE_WALL_NOT_FOUND = 400
    ERROR_CODE_WALL_CONTAINS_PAINTINGS = 401

    # Painting Error Codes (500 - 599)
    ERROR_CODE_PAINTING_NOT_FOUND = 500
    ERROR_CODE_PAINTING_CONTAINS_BG_LIGHTS = 501
    ERROR_CODE_PAINTING_CONTAINS_FG_LIGHTS = 502
    ERROR_CODE_PAINTING_CONTAINS_REAL_SIZES = 503
    ERROR_CODE_PAINTING_CONTAINS_PIC_SIZES = 504

    # Real Size Error Codes (600 - 699)
    ERROR_CODE_REAL_SIZE_NOT_FOUND = 600

    # Pic Size Error Codes (700 - 700)
    ERROR_CODE_PIC_SIZE_NOT_FOUND = 700

    # Bg Light Error Codes (800 - 899)
    ERROR_CODE_BG_LIGHT_NOT_FOUND = 800

    # Fg Light Error Codes (900 - 999)
    ERROR_CODE_FG_LIGHT_NOT_FOUND = 900

    # Icon Error Codes (1000 - 1099)
    ERROR_CODE_ICON_NOT_FOUND = 1000

    # Texture Error Codes (1100 - 1199)
    ERROR_CODE_TEXTURE_NOT_FOUND = 1100
    ERROR_CODE_DEFAULT_TEXTURE_NOT_FOUND = 1101

    # Global Settings Error Codes (1200 - 1299)
    ERROR_CODE_GLOBAL_SETTINGS_NOT_FOUND = 1200

    # Floor Error Codes (1300 - 1399)
    ERROR_CODE_FLOOR_ALREADY_EXIST = 1300
    ERROR_CODE_FLOOR_NOT_FOUND = 1301


def enum_to_string(enum):
    return enum.name.lower().replace('_', ' ').replace("cant", "can't").capitalize()

