__author__ = 'chenfeiyu'

from setuptools import setup, find_packages

# default value, need to update if using other spiders
setup(
    name='spider_robot',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = spider_robot.settings']},
)