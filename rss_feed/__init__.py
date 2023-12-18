
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from xml.etree import ElementTree as ET
import requests
from datetime import datetime, timedelta

db = SQLAlchemy()
DB_NAME = "rss_feed.db"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = 'randomsupersecretkey123'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

