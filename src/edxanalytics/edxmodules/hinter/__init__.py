"""
edInsights backend for wrong-answer-based hinting.
Currently used to display and collect crowdsourced hints, but
could be expanded to use other data.
"""

from edinsights.core.decorators import query, event_handler, view, event_property
from django.http import HttpResponse
from edinsights.core.djobject import http_rpc_helper

import json
import random


@event_handler()
def hinting_setup(mongodb, events):
    """
    Establishes a problem for hinting.
    Each event in events has:
    - location - a location tuple for the problem module.
    - user
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
        location = evt['location']

        # settings contains content-level settings for the hinter, like
        # whether to moderate.
        # Update or create it.
        new_settings = {
            'moderate': evt['moderate'],
            'display_only': evt['display_only'],
            'debug': evt['debug'],
            'location': location
        }
        settings = mongodb['settings']
        settings.update(
            {'location': location},
            new_settings,
            upsert=True
        )

        # Create a userdata, if none exists.
        userdata = mongodb['userdata']
        spec = {
            'user': evt['user'],
            'problem': location,
        }
        user = userdata.find_one(spec)
        if user is None:
            spec.update({
                'hints_shown': [],
                'previous_answers': [],
                'voted': False,
            })
            userdata.insert(spec)


@query()
def get_hint(mongodb, query, in_dict_json):
    """
    Returns hints for students to see.
    in_dict has the following keys:
    - 'location' with a location tuple for the problem.
    - 'answer' with the text of the answer.
    - 'user' with the id of the user.
    - 'number_best' - How many of the best hints to return.
    - 'number_random' - How many random hints to add to the best hints.
    Returns a list of hints.
    """
    in_dict = json.loads(in_dict_json)
    location = in_dict['location']
    answer = in_dict['answer']

    # First, make sure the answer is actually valid.
    if not query.validate_answer(json.dumps(location), answer):
        return {
            'success': False,
            'error': 'Invalid answer!'
        }

    # Generate all hints whose answers are close enough to the submitted
    # answer.
    hints = mongodb['hints']
    all_hints = hints.find({'problem': location})
    matching_hints = []
    for candidate in all_hints:
        if query.compare_answer(json.dumps(location), answer, candidate['answer']):
            matching_hints.append(candidate)

    # Now, pick the best and random hints.
    out_hints = []
    matching_hints.sort(key=lambda object: object['votes'])
    for i in xrange(min(len(matching_hints), in_dict['number_best'])):
        temp = matching_hints.pop()
        out_hints.append(temp)
    for i in xrange(min(len(matching_hints), in_dict['number_random'])):
        temp = matching_hints.pop(random.randint(0, len(matching_hints) - 1))
        out_hints.append(temp)

    # Record which hints we are going to show the user.
    out_hint_ids = [hint['_id'] for hint in out_hints]
    userspec = {
        'user': in_dict['user'],
        'problem': location,
    }
    userdata = mongodb['userdata']
    user = userdata.find_one(userspec)
    user['hints_shown'] = list(set(user['hints_shown']) | set(out_hint_ids))
    if answer not in user['previous_answers']:
        user['previous_answers'].append(answer)
    # Write the user back into the db, except remove the _id field,
    # which cannot be overwritten.
    del user['_id']
    userdata.update(userspec, {'$set': user})

    return {'success': True,
            'hints': [hint['hint'] for hint in out_hints]}


@query()
def submit_hint(mongodb, query, in_dict_json):
    """
    Adds a new hint.
    in_dict has the following keys:
    - 'location' with a location tuple for the problem.
    - 'answer' with the text of the answer.
    - 'hint' with the text of the hint that we want to add.
    - 'user' with the id of the user.
    Returns a success/failure message.
    """
    # Find the user-problem pair, making a new one if it doesn't
    # exist (that's what 'upsert' does).
    in_dict = json.loads(in_dict_json)
    location = in_dict['location']
    answer = in_dict['answer']
    userdata = mongodb['userdata']
    spec = {
        'user': in_dict['user'],
        'problem': location,
    }

    # Make sure the user is actually qualified to submit a hint.
    matching_user = userdata.find_one(spec)
    if matching_user['voted']:
        return 'Already voted!'

    problem_settings = mongodb['settings'].find_one({'location': location})
    if problem_settings is None or problem_settings['display_only']:
        return 'This problem does not accept hints!'

    if not query.validate_answer(json.dumps(location), answer):
        return 'Invalid answer!'

    # Now, add the hint to the database.
    hints = mongodb['hints']
    hints.insert({
        'problem': location,
        'answer': answer,
        'hint': in_dict['hint'],
        'user': in_dict['user'],
        'votes': 0,
        'settings': {
            'approved': False
        }
    })

    # Prevent the student from submitting more hints, but not in debug
    # mode.
    if not problem_settings['debug']:
        userdata.update(spec, {'$set': {'voted': True}})
    userdata.update(spec, {'$set': {
        'hints_shown': [],
        'previous_answers': []
    }})
    return 'Thank you for submitting a hint!'


@view()
def hinting_get_hints(mongodb):
    """ A readout test for hinting_setup """
    return mongodb['hints'].find({})


@view()
def hinting_get_users(mongodb):
    """ A readout test for hinting_setup """
    return mongodb['userdata'].find({})


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
