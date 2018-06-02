#!/bin/env bash

source ./venv/bin/activate
echo "Starting flask scrapy with nice and low i/o priority"
#ionice keep the process at low enough disk and CPU priority
nohup python2.7 flask_scrapy_manage.py runserver >/dev/null 2>&1 &
