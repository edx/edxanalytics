#!/bin/bash

# Run the main analytics server on port 9999

source ../python/bin/activate
source ../ruby/scripts/rvm
cd src/edxanalytics
while [ 1 == 1 ] ; do 
  python manage.py runserver 127.0.0.1:9999
  sleep 1
done
