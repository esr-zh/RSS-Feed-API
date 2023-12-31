"""
Handles web request routes and responses.

endpoints defined: /parse-rss and /show-data
"""


import requests
from flask import Blueprint, request, jsonify, render_template
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
        # Return existing articles if the feed was parsed less than 10 minutes ago
        articles = [{'title': article.title, 'description': article.description} for article in existing_feed.articles]
    else:
        articles_data = parse_rss_feed(url)

        if existing_feed:
            # Update last parsed time
            existing_feed.last_parsed = datetime.utcnow()
        else:
            # Create new RSS feed entry
            existing_feed = RSSFeed(url=url, last_parsed=datetime.utcnow())
            db.session.add(existing_feed)
            db.session.flush()

        # Update or add new articles
        for article_data in articles_data:
            article = Article.query.filter_by(title=article_data['title'], rss_feed_id=existing_feed.id).first()
            if article:
                # Update existing article
                article.description = article_data['description']
            else:
                # Add new article
                new_article = Article(title=article_data['title'], description=article_data['description'],
                                      rss_feed_id=existing_feed.id)
                db.session.add(new_article)

        db.session.commit()
        articles = articles_data

    return jsonify(articles)


@views.route('/show-data', methods=['GET'])
def show_data():
    # view the results of the rss feed contents using flask itself
    feeds = RSSFeed.query.all()
    return render_template('data-table.html', feeds=feeds)


def parse_rss_feed(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    articles = []

    for item in root.findall('.//item'):
        title = item.find('title').text
        description = item.find('description').text
        articles.append({'title': title, 'description': description})

    return articles
