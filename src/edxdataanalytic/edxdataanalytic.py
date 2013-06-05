from edinsights.core.decorators import query, event_handler, view, event_property
from django.contrib.auth.models import User

@view()
def sample_view():
    return "Hello"

@query()
def user_autocomplete(autocomplete):
    return [u.username for u in User.objects.filter(username__startswith='f')[:20]]
