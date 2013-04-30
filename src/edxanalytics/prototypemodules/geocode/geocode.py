''' This module adds a location to an event. 

This was added as a use case, and we discovered we need an @initialize
decorator. As a result, this code is an untested placeholder. 
'''

import os.path

import urllib2
import pygeoip
import zlib

from pkg_resources import resource_filename

gi = None

@initialize
def bootstrap():
    ''' 
    '''
    file_location = resource_filename(__name__, "data/GeoLiteCity.dat")
    if not os.path.exists(file_location):
        response = urllib2.urlopen('http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz')
        zipped_database = response.read()
        unzipped_database = zlib.decompress(zipped_database)
        f=os.open(file_location)
        f.write(unzipped_database)
        f.close()

@event_property()
def country_from_ip(fs, event):
    global gi
    if gi is None: 
        file_location = resource_filename(__name__, "data/GeoLiteCity.dat")
        gi = pygeoip.GeoIP(file_location , pygeoip.MEMORY_CACHE)
    
    return gi.record_by_addr(event['ip']).country
