from app.controllers.user_manager import admin_user_register, is_admin_exist
from app.config.user_status import UserStatus
from app import db


# Ref: https://stackoverflow.com/questions/20744277/sqlalchemy-create-all-does-not-create-tables

# Admin user registration
if is_admin_exist() is True:
    print("Admin user already added")
else:
    db.create_all()
    user_date = {
        'username' : 'AdminApp',
        'password' : 'AdminApp202!@',
        'language' : 'eng',
        'status' : UserStatus.ADMIN_USER.value
    }
    admin_user_register(data=user_date)
    print("Admin user added to database")

