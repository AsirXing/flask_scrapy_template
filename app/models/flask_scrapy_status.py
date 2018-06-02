__author__ = 'chenfeiyu'
import logging
from .. import db
from sqlalchemy import UniqueConstraint
from datetime import datetime
from spider_configure import SpiderConfigure
from ..common.exceptions import ValidationError, DBError


class FlaskScrapyStatus(db.Model):
    __tablename__ = 'flask_scrapy_status'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(17))
    spider_name = db.Column(db.String(20))
    total_times = db.Column(db.Integer, default=0)
    failed_times = db.Column(db.Integer, default=0)
    can_retry = db.Column(db.Boolean, default=True)
    __table_args__ = (
        UniqueConstraint('key', 'spider_name'),
    )

    @staticmethod
    def load_status(key, spider_name):
        if key is None or spider_name is None:
            raise ValidationError('Missing key or spider name')
        try:
            return FlaskScrapyStatus.query.filter_by(key=key, spider_name=spider_name).first()
        except Exception, e:
            raise DBError(e)

    @staticmethod
    def save_or_update(key, spider_name, isFailed):
        if key is None or spider_name is None:
            raise ValidationError('Missing key or spider name')
        spider_configure = SpiderConfigure.get(spider_name)
        if not spider_configure:
            raise ValidationError('Cannot find spider configure data')
        try:
            status = FlaskScrapyStatus.query.filter_by(key=key, spider_name=spider_name).first()
            if status:
                status.total_times = status.total_times + 1
                if isFailed:
                    status.failed_times = status.failed_times + 1
                # it always failed and exceed the maximum failed limit, then just not retry any more
                if status.total_times == status.failed_times and status.failed_times > spider_configure.accept_failed_times:
                    status.can_retry = False
            else:
                status = FlaskScrapyStatus(key=key, spider_name=spider_name, total_times=1)
                if isFailed:
                    status.failed_times = 1
                db.session.add(status)
            return status
        except Exception, e:
            raise DBError(e)