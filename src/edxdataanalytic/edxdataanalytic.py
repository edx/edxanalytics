import json

from edinsights.core.decorators import query, event_handler, view, event_property
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from mock import Mock

from courseware.model_data import ModelDataCache
from courseware.module_render import get_module_for_descriptor_internal
from xmodule.modulestore import Location
from xmodule.modulestore.django import modulestore

from capa.responsetypes import StudentInputError


@query()
def user_autocomplete(autocomplete):
    return [u.username for u in User.objects.filter(username__startswith='f')[:20]]


def get_module_edinsights(location_tuple):
    # Make a login
    # MOVE THIS SOMEWHERE ELSE BEFORE DEPLOY.
    insights_users = User.objects.filter(username='edInsights')
    if len(insights_users) == 0:
        print "Making new user for insights."
        user = User.objects.create_user('edInsights', 'felixsun@edx.org', 'edInsights')
        user.is_staff = True
        user.save()
    else:
        user = insights_users[0]

    # First, initialize the problem.
    loc = Location(location_tuple)
    course_id = loc.course_id
    descriptors = modulestore().get_items(loc)
    m_d_c = ModelDataCache(descriptors, course_id, user)

    # Arguments of get_module_for_descriptor_internal:
    # user, descripor, model data cache, course id, tracking function, xqueue url
    # The mock tracking function and empty xquque url appear to work right now,
    # so I'm not complaining.
    module = get_module_for_descriptor_internal(
        user, descriptors[0], m_d_c, course_id, Mock(), ''
    )
    return module


@query()
def compare_answer(location_json, a, b):
    """
    Compares whether a and b are equal within tolerance, according
    to the first responsetype at location_tuple.

    Returns 'true', 'false', or 'error'.
    """
    capa_module = get_module_edinsights(json.loads(location_json))
    responder = capa_module.lcp.responders.values()[0]
    try:
        return responder.compare_answer(a, b)
    except StudentInputError:
        return 'error'


@query()
def validate_answer(location_json, answer):
    """
    Determines whether answer is in a valid form for the specified problem.
    Returns 'true' if valid, 'false' otherwise.
    """
    capa_module = get_module_edinsights(json.loads(location_json))
    responder = capa_module.lcp.responders.values()[0]
    return responder.validate_answer(answer)
