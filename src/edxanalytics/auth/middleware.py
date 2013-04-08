from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings

class SecretKeyAuthenticationMiddleware():
    ''' Allows a user to be logged in by passing an appropriate secret
    key in the headers.

    Minimal testing. 
    '''
    def process_request(self, request):
        if 'HTTP_X_SECRET_KEY' in request.META:
            try: 
                valid_keys = settings.VALID_X_HEADER_KEYS
            except:
                valid_keys = []

            if request.META['HTTP_X_SECRET_KEY'] in valid_keys:
                user = User.objects.all()[0]
                user.backend = 'fake_backedn'
                login(request, user)
        
