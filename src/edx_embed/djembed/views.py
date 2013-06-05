import urlparse
import requests

from mako.template import Template

from django.http import HttpResponse
from django.conf import settings

def secret_key():
    if DEBUG:
        key = "debug_key"
    else:
        key = None
    try:
        import os
        key = os.environ['DJANALYTICS_SHARED_SECRET']
    except: 
        pass
    try: 
        key = settings.DJANALYTICS_SHARED_SECRET
    except: 
        pass
    if key:
        return key
    raise Exception("Production environments must set a secret key.")
    

def home(request):
    response = requests.get("http://127.0.0.1:9022/view/global/user_count")
    return HttpResponse(response.content)

def embed_analytics(analytic, acl):
    pass

def sysadmin_dash(request):
    output = Template(filename="template.html").render()
    return HttpResponse(output) #"<html>Hello</html>")

def url_rewrite(url, path_drops=[1], new_server = None):
    ''' Slightly hacked-together code to do URL rewriting. path_drops
    is a list of fields to drop from the URL path. E.g., for [1,3], it
    would convert:
      http://www.foo.com/patha/pathb/pathc/pathd/pathe
    To:                    1     2     3     4     5
      http://www.bar.com/pathb/pathd/pathe
                           2     4     5
    new_server replaces www.bar.com
    
    url is the original URL. 
    '''
    parse = urlparse.urlparse(url)
    path = parse.path.split("/")
    if path_drops:
        for i in path_drops:
            path.pop(i)
    new_path="/".join(path)
    new_parse = [p for p in parse]
    new_parse[2] = new_path
    if new_server: 
        new_parse[1] = new_server
    new_url = urlparse.urlunparse(new_parse)
    print new_url
    return new_url

def proxy(request):
    ''' This is a proxy to a djanalytics server. The goal is to be
    able to route AJAX calls, without the client knowing about the SOA
    layer, and eventually, to add ACLs, and to rewrite available
    analytics based on a config file, '''
    headers = { 'x-static-root': '/static/djdash/' }
    try: 
        headers['x-secret-key'] = secret_key()
    except:
        pass

    new_location = url_rewrite(request.build_absolute_uri(), 
                               new_server = "127.0.0.1:9022")
    dja_response = requests.get(new_location, headers = headers)
    response = HttpResponse(dja_response.content)
    if 'content-type' in dja_response.headers:
        response['content-type'] = dja_response.headers['content-type']
    return response
