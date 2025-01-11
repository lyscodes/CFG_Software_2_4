import os
from sqlalchemy import create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
from authlib.integrations.flask_client import OAuth
from flask_bcrypt import Bcrypt
from app.routes import main

db = SQLAlchemy()
oauth = OAuth()
bcrypt = Bcrypt()


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('settings.py')

    app.jinja_env.lstrip_blocks = True

    app.jinja_env.trim_blocks = True

    db = SQLAlchemy(app)

    migrate = Migrate(app, db)

    db.init_app(app)
    oauth.init_app(app)
    bcrypt.init_app(app)

    engine = create_engine(os.getenv('CONNECTION_STRING'))

    # using SQLite will not require this
    if not database_exists(engine.url):
        create_database(engine.url)

    app.register_blueprint(main)

    return app