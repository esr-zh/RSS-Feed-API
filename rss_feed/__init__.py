
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from xml.etree import ElementTree as ET
import requests
from datetime import datetime, timedelta

db = SQLAlchemy()
DB_NAME = "rss_feed.db"
SK = "randomsupersecretkey123"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = f'{SK}'

    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app

