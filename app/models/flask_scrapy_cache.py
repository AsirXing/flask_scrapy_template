__author__ = 'chenfeiyu'
import logging
from sqlalchemy import UniqueConstraint
from .. import db
from datetime import datetime
from ..common.exceptions import ValidationError, DBError


class FlaskScrapyCache(db.Model):
    __tablename__ = 'flask_scrapy_cache'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(17))
    spider_name = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    xml = db.Column(db.Text)
    __table_args__ = (
        UniqueConstraint('key', 'spider_name'),
    )

    @staticmethod
    def load_cache(key, spider_name):
        if key is None or spider_name is None:
            raise ValidationError('Missing key or spider name')
        try:
            return FlaskScrapyCache.query.filter_by(key=key, spider_name=spider_name).first()
        except Exception, e:
            raise DBError(e)

    @staticmethod
    def save_or_update(key, spider_name, xml):
        if xml is None:
            # not save empty data in this table
            return
        try:
            cache = FlaskScrapyCache.query.filter_by(key=key, spider_name=spider_name).first()
            if cache:
                if cache.xml != xml:
                    cache.xml = xml
                    cache.date = datetime.utcnow()
            else:
                cache = FlaskScrapyCache(key=key, spider_name=spider_name, xml=xml)
                db.session.add(cache)
            return cache
        except Exception, e:
            raise DBError(e)