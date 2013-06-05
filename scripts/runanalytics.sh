#!/bin/bash

# Set up an analytics development environment This script doesn't work
# post-moving-directories. Please ignore it (or fix it).

echo "Sorry; this script won't work"

source python/bin/activate
source ruby/scripts/rvm

cd djanalytics
python setup.py install
cd ../loghandlersplus
python setup.py install
cd ../djeventstream
python setup.py install

xterm -e ./mitxanalytics.sh &
xterm -e ./edxanalytics.sh &
sleep 10