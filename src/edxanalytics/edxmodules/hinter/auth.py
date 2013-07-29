"""
Implements simple token checking for the hinter module.
"""
from django.http import HttpResponse
from django.conf import settings
import json


def token_check(f):
    """
    Allows a request through only if its header has the correct
    password.
    """
    def wrapped_f(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION') != settings.PASSWORD:
            return HttpResponse(json.dumps({
                'success': False,
                'error': 'Improper login with edInsights!'
            }))
        return f(request, *args, **kwargs)
    return wrapped_f