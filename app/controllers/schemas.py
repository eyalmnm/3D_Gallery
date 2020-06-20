from marshmallow import Schema, fields


# ==================================   User  ==================================
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegistrationSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    language = fields.Str(required=False)
    status = fields.Int(required=True)


class GetUserIdRemotelySchema(Schema):
    key = fields.Str(required=True)


# ==================================   Room  ==================================
class AddRoomSchema(Schema):
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)
    uuid = fields.Str(required=True)


class GetRoomByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateRoomByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)


class DeleteRoomByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Wall  ==================================
class AddWallSchema(Schema):
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)
    uuid = fields.Str(required=True)
    room_id = fields.Int(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)


class GetWallByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateWallByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    texture_id = fields.Int(required=True)
    name = fields.Str(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)


class DeleteWallByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Painting  ==================================
class AddPaintingSchema(Schema):
    wall_id = fields.Int(required=True)
    name = fields.Str(required=True)
    detail = fields.Str(required=False)
    uuid = fields.Str(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)


class GetPaintingByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdatePaintingByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    detail = fields.Str(required=False)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)


class DeletePaintingByIdShema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Real Size  ==================================
class AddRealSizeSchema(Schema):
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class GetRealSizeByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateRealSizeByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class DeleteRealSizeByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Pic Size  ==================================
class AddPicSizeSchema(Schema):
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class GetPicSizeByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdatePicSizeByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class DeletePicSizeByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Bg Light  ==================================
class AddBgLightSchema(Schema):
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    width = fields.Float(required=True)
    color = fields.Int(required=True)


class GetBgLightByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateBgLightByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    width = fields.Float(required=True)
    color = fields.Int(required=True)


class DeleteBgLightByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Fg Light  ==================================
class AddFgLightSchema(Schema):
    uuid = fields.Str(required=True)
    painting_id = fields.Int(required=True)
    color = fields.Int(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)


class GetFgLightByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateFgLightByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    color = fields.Int(required=True)
    x_pos = fields.Float(required=True)
    y_pos = fields.Float(required=True)
    z_pos = fields.Float(required=True)


class DeleteFgLightByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Icon  ==================================
class AddNewIconSchema(Schema):
    uuid = fields.Str(required=True)
    user_id = fields.Int(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class GetIconByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateIconByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class DeleteIconByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


# ==================================   Texture  ==================================
class AddNewTextureSchema(Schema):
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class GetTextureByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateTextureByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class DeleteTextureByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class GetDefaultRoomTextureSchema(Schema):
    uuid = fields.Str(required=True)


class UpdateDefaultRoomTextureSchema(Schema):
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class GetDefaultCeilingTextureSchema(Schema):
    uuid = fields.Str(required=True)


class UpdateDefaultCeilingTextureSchema(Schema):
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


class GetDefaultWallTextureSchema(Schema):
    uuid = fields.Str(required=True)


class UpdateDefaultWallTextureSchema(Schema):
    uuid = fields.Str(required=True)
    src = fields.Str(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)


# ==================================   Global Settings  ==================================
class SaveGlobalSettingsSchema(Schema):
    uuid = fields.Str(required=True)
    floor_texture_index = fields.Int(required=True)
    wall_texture_index = fields.Int(required=True)
    startup_room_index = fields.Int(required=True)
    floor_texture_name = fields.Str(required=True)
    wall_texture_name = fields.Str(required=True)


class GetGlobalSettingsByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class GetGlobalSettingsDataSchema(Schema):
    uuid = fields.Str(required=False)
    # username = fields.Str(required=True)
    # password = fields.Str(required=True)
