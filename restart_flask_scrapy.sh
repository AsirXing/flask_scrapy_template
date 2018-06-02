#!/usr/bin/env bash

#kill all processes of flask_scrapy_manage.py
pkill -9 -f flask_scrapy_manage.py
#Give them a chance to shut down gracefully.
echo "Sleeping for 5 seconds to allow graceful thread completion"
sleep 5;
#Clear out logs every time this is run. NOte not error log
echo "Clearing info logs"
>| ./log/python.log
bash ./start_flask_scrapy.sh
