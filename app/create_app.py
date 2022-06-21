from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def create_app():
    import config
    from routes import api

    flask_app = Flask(__name__)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_CONNECTION_URI
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.config["SECRET_KEY"] = config.secret_key

    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()
        flask_app.register_blueprint(api, url_prefix="/api")

    return flask_app
