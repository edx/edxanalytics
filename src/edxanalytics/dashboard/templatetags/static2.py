from django import template
import auth.middleware

register = template.Library()

from urlparse import urljoin

@register.simple_tag
def static2(path):
    return urljoin(auth.middleware.overloads['STATIC_URL'], path) # 

