import os

# Ref: https://stackoverflow.com/questions/50846856/in-flask-sqlalchemy-how-do-i-set-check-same-thread-false-in-config-py

basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    # The key is Sha-256 of 3D_Gallery_Israel_Raanana_em-projects_2020_03_14 (https://emn178.github.io/online-tools/sha256.html)
    SECRET_KEY = os.environ.get('SECRET_KEY') or '0ecdbc974e2602241e995cd30e790f3b8524187a224231abf5285e7c3911dd0e'

    # SQLite Configuration
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                             'app.db')) + '?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Current Configuration
    ENV = 'DEV'  # DEV or PRO
