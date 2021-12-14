import secrets


class InitConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///auth.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = secrets.token_urlsafe(32)

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USERNAME = "japandomitori@gmail.com"
    MAIL_PASSWORD = "7578Oo08"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
