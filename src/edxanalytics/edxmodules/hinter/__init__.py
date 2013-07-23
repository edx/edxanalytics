"""
edInsights backend for wrong-answer-based hinting.
Currently used to display and collect crowdsourced hints, but
could be expanded to use other data.
"""

from edinsights.core.decorators import query, event_handler, view, event_property
from django.http import HttpResponse
from edinsights.core.djobject import http_rpc_helper
import json
# from edxdataanalytic.edxdataanalytic import user_autocomplete


@event_handler()
def hinting_setup(mongodb, events):
    """
    Establishes a problem for hinting.
    Each event in events has:
    - location - a location tuple for the hinter module.
    - moderate - True or False - controls whether moderation is
      enabled for this hinting instance.
    - display_only - if True, we will not ask people to submit or vote
      for hints.  Only instructor-specified hints will be shown.
          - A True setting makes moderate meaningless.
    - debug - if True, allow users to submit as many hints and vote as many
      times as they want.
    """
    for evt in events:
        # Make a location tag.
        location = evt['problem_location']

        # settings contains content-level settings for the hinter, like
        # whether to moderate.
        # Update or create it.
        settings = mongodb['settings']
        problem_settings = settings.find({'location': location})
        new_settings = {
            'moderate': evt['moderate'],
            'display_only': evt['display_only'],
            'debug': evt['debug']
        }
        if len(list(problem_settings)) > 0:
            problem_settings.update({}, new_settings)
        else:
            # Make a new settings document.
            new_settings.update({'location': location})
            settings.insert(new_settings)

@query()
def submit_hint(mongodb, query, in_dict):
    """
    Adds a new hint.
    in_dict has the following keys:
    - 'answer' with the text of the answer.
    - 'hint' with the text of the hint that we want to add.
    - 'user' with the username of the user.
    """
    pass


@view()
def hinting_get_settings(mongodb):
    """ A readout test for hinting_setup """
    return mongodb['settings'].find({})

@view()
def hinting_hello(query):
    ''' Tests edxdataanalytic calls.'''
    out = query.validate_answer(
        json.dumps(['i4x', 'Me', '19.002', 'problem', 'Numerical_Input']),
        '12',
    )
    if out == 'true':
        return HttpResponse('Yes')
    else:
        return HttpResponse('No')
