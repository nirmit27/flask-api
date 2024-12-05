from os import environ, path
from dotenv import load_dotenv

from flask import Flask
from flask_login import LoginManager

from .models import db, User
from .auth.routes import auth_bp
from .views.routes import view_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{environ.get('DB_NAME')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    create_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix="/user/auth")
    app.register_blueprint(view_bp, url_prefix="/")

    return app


def create_db(app):
    if not path.exists(f"instance/{environ.get('DB_NAME')}"):
        with app.app_context():
            db.create_all()
        print(f"\nDatabase created")
