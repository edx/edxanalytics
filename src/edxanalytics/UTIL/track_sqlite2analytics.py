#!/usr/bin/python
#
# spool tracking logs from sqlite3 to edX analytics
#

import os, sys, string, re
import json
import sqlite3
import requests
from collections import OrderedDict
from urllib import urlencode

import logging, logging.handlers

logging.handlers.HTTPHandler('','',method='GET')
logger = logging.getLogger('simple_example') 
http_handler = logging.handlers.HTTPHandler('127.0.0.1:9022', '/httpevent', method='GET') 
logger.addHandler(http_handler)


dbfn = '../db/mitx.db'
anaurl = "http://localhost:9022/httpevent"

con = sqlite3.connect(dbfn)
con.row_factory = sqlite3.Row
    
cur = con.cursor()    
cur.execute('SELECT * from track_trackinglog order by dtcreated ASC')
    
def send_event(event):
    if 0:
        logger.critical(event)
    else:
        params = urlencode({'msg': event})
        # print params
        resp = requests.get('%s?%s' % (anaurl, params))
        # print resp.content

cnt = 0
while True:
    data = cur.fetchone()
    if data is None:
        break
    # print data.keys()
    event = json.dumps(OrderedDict(data))
    send_event(event)
    cnt += 1
    if cnt%100 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
    #if cnt>100:
    #    break

print "Done!"
    
