from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import InitConfig

from register_app.model import db, UserModel
from register_app.view import main_blueprint
from register_app.auth.view import auth_blueprint, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(InitConfig)
    migrate = Migrate()
    login_manager = LoginManager()

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    return app
