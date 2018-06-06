# Extend New Spider
To extend a new spider. See the existing spider examples in ./spiders/

1. Create your own spider in ./spiders/spider_robot/spiders like the existing spiders
2. Create your own items in ./spiders/spider_robot/items.py, the item depends on what your original data have.
3. Configure your spider in ./spiders/spider_manager.py  and ./common/constants.py
4. Add your new spider in table spider_configure or put in flask_scrapy_manager.py deploy method
```
INSERT IGNORE INTO `spider_configure` (`spider_name`) VALUES ('test_spider');
```

# Deploy this python project

Latest update: upgrade project to Python 3.6 and Scrapy 1.5.0

v2.0: Python 3.6 and Scrapy 1.5.0

v1.0: Python 2.7 and Scrapy 1.0.3

The following steps are all based on v1.0:

1. Install sqlite
```
sudo yum install sqlite-devel -y
```

2. If missing Twisted
```
wget https://pypi.python.org/packages/source/T/Twisted/Twisted-15.2.1.tar.bz2
tar -xjvf Twisted-15.2.1.tar.bz2
cd Twisted-15.2.1
python2.7 setup.py install
```

3. Install dependency
```
sudo yum install -y libffi libffi-devel libxslt-devel libxml2-devel
```

4. install python2.7
```
wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar -xzf Python-2.7.6.tgz  
cd Python-2.7.6
./configure --prefix=/usr/local
make && make install
python2.7 setup install
```

5. install tools easy_install-2.7
```
wget http://pypi.python.org/packages/source/d/distribute/distribute-0.6.35.tar.gz
tar xf distribute-0.6.35.tar.gz
cd distribute-0.6.35
python2.7 setup.py install
```

6. install pip2.7
```
easy_install-2.7 pip
```

7. go to project package/
```
virtualenv --no-site-packages venv
source venv/bin/activate
pip2.7 install -r requirements.txt
```

8. deploy & run the server
only first time deploy need to deploy migrate database

```
export DEV_DATABASE_URL='mysql+pymysql://username:password@localhost/flask_scrapy_template'

python2.7 flask_scrapy_manage.py db init
python2.7 flask_scrapy_manage.py db migrate
python2.7 flask_scrapy_manage.py db upgrade
python2.7 flask_scrapy_manage.py deploy

./start_flask_scrapy.sh
```

9. install httpie & testing
```
pip install httpie

http --auth username:secret_key GET http://localhost:5002/api/v1.0/test_flask_scrapy key=some_search_key get_latest=True
```




