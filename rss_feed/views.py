import requests
from flask import Blueprint, request, jsonify
from .auth import token_required
from .models import RSSFeed, Article, db
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

views = Blueprint('views', __name__)


@views.route('/parse-rss', methods=['POST'])
@token_required
def parse_rss():
    url = request.json['url']
    existing_feed = RSSFeed.query.filter_by(url=url).first()

    if existing_feed and datetime.now() - existing_feed.last_parsed < timedelta(minutes=10):
        articles = [{'title': article.title, 'description': article.description} for article in existing_feed.articles]
    else:
        articles_data = parse_rss_feed(url)

        if existing_feed is None:
            existing_feed = RSSFeed(url=url, last_parsed=datetime.utcnow())
            db.session.add(existing_feed)
            db.session.flush()

        existing_feed.last_parsed = datetime.utcnow()
        existing_feed.articles = []

        for article_data in articles_data:
            article = Article(title=article_data['title'], description=article_data['description'],
                              rss_feed_id=existing_feed.id)
            existing_feed.articles.append(article)

        db.session.commit()
        articles = articles_data

    return jsonify(articles)


def parse_rss_feed(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    articles = []

    for item in root.findall('.//item'):
        title = item.find('title').text
        description = item.find('description').text
        articles.append({'title': title, 'description': description})

    return articles
