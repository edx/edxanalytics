#!/bin/bash

cd ../src/edxanalytics
python manage.py runserver 127.0.0.1:9999 &
sleep 1

cd /Users/juhokim/edx_all/edx-platform
django-admin.py runserver --settings=lms.envs.analyticsserver --pythonpath=. 127.0.0.1:9012 &
sleep 1

