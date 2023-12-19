"""
Observing the endpoints for

-Testing for an Existing RSS Feed (Not Re-Parsed within 10 minutes)
-Testing for RSS Feed Re-Parsing (After 10 minutes)
-Testing Invalid URL Handling
-Testing Unauthorized Access (Without JWT Token)

"""

import pytest
from rss_feed import create_app, db
from rss_feed.models import RSSFeed, Article
from datetime import datetime, timedelta
from unittest.mock import patch


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def add_sample_feed(client):
    with client.application.app_context():
        feed = RSSFeed(url='http://www.cbsnews.com/latest/rss/main', last_parsed=datetime.utcnow())
        article = Article(title='Sample Article', description='Sample Description', rss_feed=feed)
        db.session.add(feed)
        db.session.add(article)
        db.session.commit()


def test_existing_rss_feed_not_reparsed(client):
    add_sample_feed(client)
    response = client.post('/parse-rss', json={'url': 'http://www.cbsnews.com/latest/rss/main'})
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['title'] == 'Sample Article'


def test_rss_feed_reparsing(client):
    add_sample_feed(client)
    with client.application.app_context():
        feed = RSSFeed.query.first()
        feed.last_parsed = datetime.utcnow() - timedelta(minutes=11)
        db.session.commit()

    with patch('rss_feed.views.parse_rss_feed') as mock_parse:
        mock_parse.return_value = [{'title': 'New Article', 'description': 'New Description'}]
        response = client.post('/parse-rss', json={'url': 'http://www.cbsnews.com/latest/rss/main'})
        assert response.status_code == 200
        data = response.get_json()
        assert data[0]['title'] == 'New Article'


def test_invalid_url(client):
    response = client.post('/parse-rss', json={'url': 'invalid-url'})
    assert response.status_code != 200


def test_unauthorized_access(client):
    # This test assumes that your API requires a JWT token for the /parse-rss endpoint
    response = client.post('/parse-rss', json={'url': 'http://www.cbsnews.com/latest/rss/main'})
    assert response.status_code == 403
