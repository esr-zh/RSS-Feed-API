# simple test file to test /parse-rss

import pytest
from rss_feed import create_app, db
from rss_feed.models import RSSFeed, Article


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_parse_rss_endpoint(client):
    # Test to ensure the parse-rss endpoint works as expected
    response = client.post('/parse-rss', json={'url': 'http://www.cbsnews.com/latest/rss/main'})
    assert response.status_code == 200
