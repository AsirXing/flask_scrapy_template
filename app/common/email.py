__author__ = 'chenfeiyu'
import logging
from threading import Thread
from flask import current_app, render_template, url_for
from flask_mail import Message
from app import mail


class Email():

    @staticmethod
    def send_async_email(app, msg):
        with app.app_context():
            logging.debug('Sending email : %s' % msg)
            mail.send(msg)

    @staticmethod
    def send_email(to, subject, template, **kwargs):
        try:
            app = current_app._get_current_object()
            msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=app.config['MAIL_SENDER'], recipients=[to])
            msg.body = render_template(template + '.txt', **kwargs)
            msg.html = render_template(template + '.html', **kwargs)
            mail.send(msg)
            # thr = Thread(target=Email.send_async_email, args=[app, msg])
            # thr.start()
            # return thr
        except Exception as e:
            logging.error('Sending email failed.')
            logging.error(e)