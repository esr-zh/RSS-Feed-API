from flask import Blueprint, render_template, request, flash, jsonify
from .auth import token_required
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/parse-rss', methods=['POST'])
@token_required
def parse_rss():
    url = request.json['url']
    existing_feed = RSSFeed.query.filter_by(url=url).first()

    if existing_feed and datetime.now() - existing_feed.last_parsed < timedelta(minutes=10):
        articles = [{'title': article.title, 'description': article.description} for article in existing_feed.articles]
    else:
        articles = parse_rss_feed(url)
        # Store in database (not shown for brevity)

    return jsonify(articles)
