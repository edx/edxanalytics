#!/bin/bash

EDXANALYTICS_DIR=/Users/juhokim/edx-vagrant/edxanalytics
#EDXANALYTICS_DIR=/home/juhokim/edx-vagrant/edxanalytics
EDXANALYTICS_PORT=9999
LMS_DIR=/Users/juhokim/edx_all/edx-platform
#LMS_DIR=/home/juhokim/edx-platform
LMS_PORT=8000

cd $EDXANALYTICS_DIR/src/edxanalytics
python manage.py runserver 0.0.0.0:$EDXANALYTICS_PORT &
sleep 1

cd $LMS_DIR
rake lms[analyticsserver_dev,0.0.0.0:$LMS_PORT] &
#django-admin.py runserver --settings=lms.envs.analyticsserver_dev --pythonpath=. 0.0.0.0:$LMS_PORT &
sleep 1
