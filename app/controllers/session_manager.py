from app.services.gallery3d_sevice import get_user_id_ext
from app import db
from app.models import Session, User


def get_user_id(uuid):
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        user_id = session.email
        if user_id:
            return user_id
        else:
            return None
    else:
        user_id = get_user_id_ext(uuid=uuid)
        if user_id:
            try:
                session = db.session.query(Session).filter_by(email=str(user_id)).first()
            except Exception as ex:
                print('ex: ' + ex)
            if session:
                session.uuid = uuid
                session = session.update_session()
            else:
                session = Session(username=user_id, uuid=uuid)
                session = session.save()
            return session.email
        else:
            return None
