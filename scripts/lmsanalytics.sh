#!/bin/bash

# Runs LMS-embedded analytics on port 9012

source ../python/bin/activate
source ../ruby/scripts/rvm
cd ../mitx
pwd
while [ 1 == 1 ] ; do 
  django-admin.py runserver --settings=lms.envs.analyticsserver --pythonpath=. 127.0.0.1:9012
  sleep 1
done
