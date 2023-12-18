from . import db


class RSSFeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True, nullable=False)
    last_parsed = db.Column(db.DateTime, nullable=False)
    articles = db.relationship('Article', backref='rss_feed', lazy=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rss_feed_id = db.Column(db.Integer, db.ForeignKey('rss_feed.id'), nullable=False)
