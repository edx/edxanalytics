#!/bin/bash

EDXANALYTICS_DIR=/opt/edx-vagrant/edxanalytics
EDXANALYTICS_PORT=9999
LMS_DIR=/opt/edx/edx-platform
LMS_PORT=8000

cd $EDXANALYTICS_DIR/src/edxanalytics
python manage.py runserver 0.0.0.0:$EDXANALYTICS_PORT &
sleep 1

cd $LMS_DIR
rake lms[analyticsserver_dev,0.0.0.0:$LMS_PORT] &
#django-admin.py runserver --settings=lms.envs.analyticsserver_dev --pythonpath=. 127.0.0.1:9012 &
sleep 1
