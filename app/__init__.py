import os
from sqlalchemy import create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
from authlib.integrations.flask_client import OAuth
from flask_bcrypt import Bcrypt
from settings import Config
from dotenv import load_dotenv

db = SQLAlchemy()
oauth = OAuth()
bcrypt = Bcrypt()


def create_app(config_class=Config):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)

    app.jinja_env.lstrip_blocks = True

    app.jinja_env.trim_blocks = True

    #db = SQLAlchemy(app)
    #migrate = Migrate(app, db)

    db.init_app(app)
    oauth.init_app(app)
    bcrypt.init_app(app)

    load_dotenv

    #engine = create_engine(os.getenv('CONNECTION_STRING'))
    # using SQLite will not require this
    #if not database_exists(engine.url):
     #   create_database(engine.url)

    from app.routes import main

    app.register_blueprint(main)

    return app