from datetime import datetime, timedelta

# Install PyJWT
import jwt

from app import app
from app import db


class Defaults(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_type = db.Column(db.Integer(), nullable=False)
    item_id = db.Column(db.Integer(), nullable=False)

    def __init__(self, item_type, item_id):
        self.item_type = item_type
        self.item_id = item_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_default(self):
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<Default {}>'.format(self.item_type)


# Ref: https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way-part-2#toc-automate-tests
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    hash_pwd = db.Column(db.String(128), index=True, nullable=False)
    salt = db.Column(db.String(128), index=False, nullable=False)
    language = db.Column(db.String(8), index=True, nullable=False, default='en')
    status = db.Column(db.Integer(), index=True, nullable=False, default=5)
    icon = db.relationship('Icon', backref='user', lazy='dynamic')
    floors = db.relationship('Floor', backref='user', lazy='dynamic')

    def __init__(self, username, hash_pwd, salt, language, status):
        self.username = username
        self.hash_pwd = hash_pwd
        self.salt = salt
        self.language = language
        self.status = status

    def save(self, session):
        db.session.add(self)
        db.session.add(session)
        db.session.commit()

    def save_admin(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Floor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)  # ForeignKey User table
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    rooms = db.relationship('Room', backref='floor', lazy='dynamic')

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_floor(self):
        db.session.commit()

    def delete_floor(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["rooms"] = [room.to_dict() for room in self.rooms]
        return serialized

    def __repr__(self):
        return '<Floor {}>'.format(self.name)


class Icon(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)  # ForeignKey User table
    src = db.Column(db.String(512), index=True, unique=True, nullable=False)
    width = db.Column(db.Float(), index=False, nullable=False, default=0)
    height = db.Column(db.Float(), index=False, nullable=False, default=0)

    def __init__(self, user_id, src, width, height):
        self.user_id = user_id
        self.src = src
        self.width = width
        self.height = height

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_icon(self):
        db.session.commit()

    def delete_icon(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<Icon {}>'.format(self.src)


class Texture(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    src = db.Column(db.String(512), index=True, unique=False, nullable=False)
    width = db.Column(db.Float(), index=False, nullable=False, default=0)
    height = db.Column(db.Float(), index=False, nullable=False, default=0)
    walls = db.relationship('Wall', backref='texture', lazy='dynamic')
    rooms = db.relationship('Room', backref='texture', lazy='dynamic')

    def __init__(self, src, width, height):
        self.src = src
        self.width = width
        self.height = height

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_texture(self):
        db.session.commit()

    def delete_texture(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        # serialized["device"] = self.device.to_dict() if self.device else None
        serialized["walls"] = [wall.to_dict() for wall in self.walls]
        serialized["rooms"] = [room.to_dict() for room in self.rooms]
        return serialized

    def __repr__(self):
        return '<Texture {}>'.format(self.src)


class Room(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    floor_id = db.Column(db.Integer(), db.ForeignKey('floor.id'), nullable=False)  # ForeignKey User table
    texture_id = db.Column(db.Integer(), db.ForeignKey('texture.id'), nullable=False)  # ForeignKey Texture table
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    walls = db.relationship('Wall', backref='room', lazy='dynamic')

    def __init__(self, user_id, texture_id, name):
        self.user_id = user_id
        self.texture_id = texture_id
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_room(self):
        db.session.commit()

    def delete_room(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["walls"] = [wall.to_dict() for wall in self.walls]
        return serialized

    def __repr__(self):
        return '<Room {}>'.format(self.name)


class Wall(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    room_id = db.Column(db.Integer(), db.ForeignKey('room.id'), nullable=False)  # ForeignKey Room table
    texture_id = db.Column(db.Integer(), db.ForeignKey('texture.id'), nullable=False)  # ForeignKey Texture table
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    x_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    y_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    z_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    paintings = db.relationship('Painting', backref='wall', lazy='dynamic')

    def __init__(self, room_id, texture_id, name, x_pos, y_pos, z_pos):
        self.room_id = room_id
        self.texture_id = texture_id
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_wall(self):
        db.session.commit()

    def delete_wall(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        # serialized["device"] = self.device.to_dict() if self.device else None
        serialized["paintings"] = [painting.to_dict() for painting in self.paintings]
        return serialized

    def __repr__(self):
        return '<Wall {}>'.format(self.name)


class Painting(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    wall_id = db.Column(db.Integer(), db.ForeignKey('wall.id'), nullable=False)  # ForeignKey Wall table
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    detail = db.Column(db.String(1024), index=False, unique=False, nullable=True)
    x_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    y_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    z_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    real_sizes = db.relationship('RealSize', backref='painting', lazy='dynamic')
    pic_sizes = db.relationship('PicSize', backref='painting', lazy='dynamic')
    bg_lights = db.relationship('BgLight', backref='painting', lazy='dynamic')
    fg_lights = db.relationship('FgLight', backref='painting', lazy='dynamic')

    def __init__(self, wall_id, name, detail, x_pos, y_pos, z_pos):
        self.wall_id = wall_id
        self.name = name
        self.detail = detail
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_painting(self):
        db.session.commit()

    def delete_painting(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        # serialized["device"] = self.device.to_dict() if self.device else None
        serialized["real_sizes"] = [real_size.to_dict() for real_size in self.real_sizes]
        serialized["pic_sizes"] = [pic_size.to_dict() for pic_size in self.pic_sizes]
        serialized["bg_lights"] = [bg_light.to_dict() for bg_light in self.bg_lights]
        serialized["fg_lights"] = [fg_light.to_dict() for fg_light in self.fg_lights]
        return serialized

    def __repr__(self):
        return '<Painting {}>'.format(self.name)


class RealSize(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    painting_id = db.Column(db.Integer(), db.ForeignKey('painting.id'), nullable=False)  # ForeignKey Painting table
    width = db.Column(db.Float(), index=False, nullable=False, default=0)
    height = db.Column(db.Float(), index=False, nullable=False, default=0)

    def __init__(self, painting_id, width, height):
        self.painting_id = painting_id
        self.width = width
        self.height = height

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_real_size(self):
        db.session.commit()

    def delete_real_size(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<RealSize {}>'.format(self.id)


class PicSize(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    painting_id = db.Column(db.Integer(), db.ForeignKey('painting.id'), nullable=False)  # ForeignKey Painting table
    width = db.Column(db.Float(), index=False, nullable=False, default=0)
    height = db.Column(db.Float(), index=False, nullable=False, default=0)

    def __init__(self, painting_id, width, height):
        self.painting_id = painting_id
        self.width = width
        self.height = height

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_pic_size(self):
        db.session.commit()

    def delete_pic_size(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<PicSize {}>'.format(self.id)


class BgLight(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    painting_id = db.Column(db.Integer(), db.ForeignKey('painting.id'), nullable=False)  # ForeignKey Painting table
    width = db.Column(db.Float(), index=False, nullable=False, default=0)
    color = db.Column(db.String(16), index=True, nullable=False, default=0)

    def __init__(self, painting_id, width, color):
        self.painting_id = painting_id
        self.width = width
        self.color = color

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_bg_light(self):
        db.session.commit()

    def delete_bg_light(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<BgLight {}>'.format(self.color)


class FgLight(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    painting_id = db.Column(db.Integer(), db.ForeignKey('painting.id'), nullable=False)  # ForeignKey Painting table
    color = db.Column(db.String(16), index=True, nullable=False, default=0)
    x_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    y_pos = db.Column(db.Float(), index=False, nullable=False, default=0)
    z_pos = db.Column(db.Float(), index=False, nullable=False, default=0)

    def __init__(self, painting_id, color, x_pos, y_pos, z_pos):
        self.painting_id = painting_id
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_fg_light(self):
        db.session.commit()

    def delete_fg_light(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<FgLight {}>'.format(self.color)


class Session(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    uuid = db.Column(db.String(128), index=True, unique=True, nullable=False)

    def __init__(self, username, uuid):
        self.email = username
        self.uuid = uuid

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_session(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Session {}>'.format(self.email)


class GlobalSettings(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    floor_texture_index = db.Column(db.Integer(), db.ForeignKey('texture.id'), nullable=False, default=0)
    wall_texture_index = db.Column(db.Integer(), db.ForeignKey('texture.id'), nullable=False, default=0)
    startup_room_index = db.Column(db.Integer(), db.ForeignKey('room.id'), nullable=False, default=0)
    floor_texture_name = db.Column(db.String(256), index=False, unique=False, nullable=False, default=0)
    wall_texture_name = db.Column(db.String(256), index=False, unique=False, nullable=False, default=0)

    def __init__(self, floor_texture_index, wall_texture_index, startup_room_index, floor_texture_name,
                 wall_texture_name):
        self.floor_texture_index = floor_texture_index
        self.wall_texture_index = wall_texture_index
        self.startup_room_index = startup_room_index
        self.floor_texture_name = floor_texture_name
        self.wall_texture_name = wall_texture_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_global_settings(self):
        db.session.commit()

    def delete_global_settings(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<GlobalSettings {}>'.format(self.floor_texture_name)
