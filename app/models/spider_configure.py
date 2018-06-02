__author__ = 'chenfeiyu'

import logging
from .. import db
from ..common.exceptions import ValidationError, DBError
from ..common.constants import Constants


class SpiderConfigure(db.Model):
    __tablename__ = 'spider_configure'
    id = db.Column(db.Integer, primary_key=True)
    spider_name = db.Column(db.String(20), unique=True)
    state = db.Column(db.String(10), default=Constants.VALUE_STATE_ON)
    accept_failed_times = db.Column(db.Integer, default=10)
    email_alert = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {'spider': self.spider_name, 'state': self.state}

    @staticmethod
    def get(spider_name):
        try:
            return SpiderConfigure.query.filter_by(spider_name=spider_name).first()
        except Exception, e:
            raise DBError(e)

    @staticmethod
    def add_spider(name):
        try:
            configure = SpiderConfigure.get(name)
            if configure is None:
                new_configure = SpiderConfigure(spider_name=name)
                db.session.add(new_configure)
                db.session.commit()
        except Exception, e:
            db.session.rollback()
            raise DBError(e)
        finally:
            db.session.close()
            db.session.remove()

    @staticmethod
    def close_spider(spider_name):
        # DB seesion needs to be commit here or it won't work
        # This is a bug needs to be fixed later
        try:
            spider_configure = SpiderConfigure.query.filter_by(spider_name=spider_name).first()
            if spider_configure.state == Constants.VALUE_STATE_ON:
                spider_configure.state = Constants.VALUE_STATE_OFF
                db.session.commit()
                return True
            else:
                return False
        except Exception, e:
            db.session.rollback()
            raise DBError(e)
        finally:
            db.session.close()
            db.session.remove()

    @staticmethod
    def disable_email_alert(spider_name):
        try:
            spider_configure = SpiderConfigure.query.filter_by(spider_name=spider_name).first()
            if not spider_configure.email_alert:
                spider_configure.email_alert = True
                db.session.commit()
        except Exception, e:
            db.session.rollback()
            raise DBError(e)
        finally:
            db.session.close()
            db.session.remove()

    @staticmethod
    def get_all_spiders():
        try:
            return SpiderConfigure.query.all()
        except Exception, e:
            raise DBError(e)

    @staticmethod
    def get_all_live_spiders():
        try:
            return SpiderConfigure.query.filter_by(state=Constants.VALUE_STATE_ON).all()
        except Exception, e:
            raise DBError(e)

    @staticmethod
    def get_all_live_spider_names():
        try:
            return [r.spider_name for r in SpiderConfigure.query.with_entities(SpiderConfigure.spider_name
                                                            ).filter_by(state=Constants.VALUE_STATE_ON).all()]
        except Exception, e:
            raise DBError(e)

    @staticmethod
    def turn_on(spider_names):
        if not spider_names:
            raise ValidationError('Missing spider names')
        try:
            for spider_name in spider_names:
                spider_configure = SpiderConfigure.query.filter_by(spider_name=spider_name).first()
                if spider_configure and spider_configure.state == Constants.VALUE_STATE_OFF:
                    spider_configure.state = Constants.VALUE_STATE_ON
        except Exception, e:
            raise DBError(e)

    @staticmethod
    def turn_off(spider_names):
        if not spider_names:
            raise ValidationError('Missing spider names')
        try:
            for spider_name in spider_names:
                spider_configure = SpiderConfigure.query.filter_by(spider_name=spider_name).first()
                if spider_configure and spider_configure.state == Constants.VALUE_STATE_ON:
                    spider_configure.state = Constants.VALUE_STATE_OFF
        except Exception, e:
            raise DBError(e)