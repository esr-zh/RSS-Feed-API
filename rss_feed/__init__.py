import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from xml.etree import ElementTree as ET
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

def parse_rss_feed(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    articles = []

    for item in root.findall('.//item'):
        title = item.find('title').text
        description = item.find('description').text
        articles.append({'title': title, 'description': description})

    return articles