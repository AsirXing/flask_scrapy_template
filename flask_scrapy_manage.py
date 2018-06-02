__author__ = 'chenfeiyu'
import os
from app import create_app, db
import logging, logging.config, yaml
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app.models.spider_configure import SpiderConfigure
from app.common.constants import Constants

app = create_app(os.getenv('FLASK_SCRAPY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db, directory='db/migrations')


# python manage.py deploy
@manager.command
def deploy():
    print("Run deployment tasks")
    # TODO enable your new spider here
    SpiderConfigure.add_spider(Constants.SPIDER_NAME_TEST_SPIDER)


def make_shell_context():
    return dict(app=app, db=db)  # these objects can be used in shell


manager.add_command("shell", Shell(make_context=make_shell_context))  # python manage.py shell

# first time run
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
manager.add_command('db', MigrateCommand)  # python manage.py db (init / upgrade / migrate -m "initial migration")


# python manage.py runserver
if __name__ == '__main__':
    # logging.basicConfig(filename='./log/error.log',level=logging.DEBUG)
    logging.config.dictConfig(yaml.load(open('./log/logging.conf')))

    # output log to file
    error_log_file = logging.getLogger('error_file')
    # error_log_file.error("Error FILE")

    info_log_file = logging.getLogger('info_file')
    # info_log_file.info("Info FILE")

    # logconsole = logging.getLogger('console')
    # logconsole.debug("Debug CONSOLE")
    # app.run(host='0.0.0.0', port=5001, debug=None, threaded=True)
    manager.add_command('runserver', Server(host='localhost', port=5002))
    # manager.add_command('runserver', Server(host='192.168.3.51', port=5002))
    manager.run()