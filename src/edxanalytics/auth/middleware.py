from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from urlparse import urljoin

overloads = {}

class SecretKeyAuthenticationMiddleware():
    ''' Allows a user to be logged in by passing an appropriate secret
    key in the headers.

    Minimal testing. 
    '''
    def process_request(self, request):
        ''' 
        '''
        ## Log in users with valid secret key
        if 'HTTP_X_SECRET_KEY' in request.META:
            try: 
                valid_keys = settings.VALID_X_HEADER_KEYS
            except:
                valid_keys = []

            if request.META['HTTP_X_SECRET_KEY'] in valid_keys:
                user = User.objects.all()[0]
                user.backend = 'fake_backedn'
                login(request, user)
            else:
                raise SuspiciousOperation("Invalid key")

        if 'HTTP_X_STATIC_ROOT' in request.META:
            overloads['STATIC_URL'] = request.META['HTTP_X_STATIC_ROOT']
        else:
            overloads['STATIC_URL'] = settings.STATIC_URL


####### Dead code
##
## It doesn't work. It tries to monkey-patch Django in different ways
## to make the static tag smarter. 

#from django.templatetags.static import register, static
#import django.core.context_processors
# def overloaded_static(prefix):
#     def new_static(path):
#         print "New static called"
#         return urljoin(prefix, path)
#     return new_static

            ## Dead code for overriding static. Doesn't work. Wanted to try a more explicit technique
        # print "About to check on static"
        # ## Override static file handler 
        # ## TODO: Break out into its own middleware. 
        # ## TODO: Make less hackish
        # ## TODO: Run only with secret key
        # ## Doesn't work. /var/www/doc/Django-1.4.5/django/core/context_processors.py
        # ## /var/www/doc/Django-1.4.5/django/templatetags/static.py
        # if 'HTTP_X_STATIC_ROOT' in request.META:
        #     django.core.context_processors.static = lambda x : {'STATIC_URL' : request.META['HTTP_X_STATIC_ROOT']}
        #     print "Overloading", request.META['HTTP_X_STATIC_ROOT']
        #     print register.tags['static']
        #     register.simple_tag(overloaded_static(request.META['HTTP_X_STATIC_ROOT']), name='static')
        #     print register.tags['static']
        # else:
        #     print "Not overloading"
        #     django.core.context_processors.static = lambda x : {'STATIC_URL': settings.STATIC_URL}
        #     register.simple_tag(static, name='static')

