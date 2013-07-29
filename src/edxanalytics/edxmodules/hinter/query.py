"""
edInsights backend for wrong-answer-based hinting.
Currently used to display and collect crowdsourced hints, but
could be expanded to use other data.

Databases:
userdata - tracks user actions on problems.  Each document:
- 'user'
- 'location' - a location
- 'hints_shown' - a list of ids of hints shown
- 'previous_answers' - a list of previous answers
- 'voted' - whether the user has voted already

settings - problem-level settings.  Each document:
- 'location'
- 'moderate'
- 'display_only'
- 'debug'

hints - has all of the hints.  Each document:
- 'location'
- 'user' - the user who submitted this hint
- 'answer' - the wrong answer that this hint is for
- 'hint' - the text of the hint
- 'votes' - how many votes this hint received
- 'settings' - a subdocument:
    - 'approved' - whether the hint has been approved
"""

from edinsights.core.decorators import query, event_handler, view
from django.http import HttpResponse

from bson.objectid import ObjectId

import json
import random


@query()
def hinting_setup(mongodb, query, in_dict_json):
    """
    Establishes a problem for hinting.
    in_dict has:
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
    in_dict = json.loads(in_dict_json)
    # Make a location tag.
    location = in_dict['location']

    # settings contains content-level settings for the hinter, like
    # whether to moderate.
    # Update or create it.
    new_settings = {
        'moderate': in_dict['moderate'],
        'display_only': in_dict['display_only'],
        'debug': in_dict['debug'],
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
        'user': in_dict['user'],
        'location': location,
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
    if query.validate_answer(json.dumps(location), answer) != 'true':
        return {
            'success': False,
            'error': 'Invalid answer!'
        }
    settings = mongodb['settings']
    moderate = settings.find_one({'location': location})['moderate']

    # Generate all hints whose answers are close enough to the submitted
    # answer.
    hints = mongodb['hints']
    if moderate:
        all_hints = hints.find({'location': location,
                                'settings.approved': True})
    else:
        all_hints = hints.find({'location': location})
    matching_hints = []
    for candidate in all_hints:
        if query.compare_answer(json.dumps(location), answer, candidate['answer']) == 'true':
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
        'location': location,
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
def hint_history(mongodb, query, in_dict_json):
    """
    Gives a readout of the hints the user has seen so far,
    as well as his submissions.  (Reset whenever the user votes
    or submits a hint.)
    in_dict:
    - 'location'
    - 'user'
    """
    # Initialize user
    in_dict = json.loads(in_dict_json)
    spec = {
        'user': in_dict['user'],
        'location': in_dict['location']
    }
    userdata = mongodb['userdata']
    matching_user = userdata.find_one(spec)
    if matching_user is None:
        return {'success': False,
                'error': 'Invalid user!'}

    # Populate a list of [id, answer, hint] tuples.
    hints = mongodb['hints']
    hints_shown = []
    for past_id in matching_user['hints_shown']:
        hint = hints.find_one({'_id': past_id})
        if hint is None:
            # Perhaps someone deleted the hint already.  Oh well.
            continue
        hints_shown.append([str(past_id), hint['answer'], hint['hint']])

    # Return the stuff.
    return {'success': True,
            'hints_shown': hints_shown,
            'previous_answers': matching_user['previous_answers']}


@query()
def vote(mongodb, query, in_dict_json):
    """
    Tallies a user vote for a single hint.
    in_dict:
    - 'location'
    - 'user'
    - 'id' of the hint we are voting for.
    """
    # Verify that the user is eligible to vote.
    in_dict = json.loads(in_dict_json)
    location = in_dict['location']
    spec = {
        'user': in_dict['user'],
        'location': location
    }
    userdata = mongodb['userdata']
    matching_user = userdata.find_one(spec)
    if matching_user is None:
        return {'success': False,
                'error': 'Invalid user!'}
    if matching_user['voted']:
        return {'success': False,
                'error': 'Already voted!'}

    # Tally the vote
    hints = mongodb['hints']
    hintspec = {'_id': ObjectId(in_dict['id'])}
    hint = hints.find_one(hintspec)
    if hint is None:
        return {'success': False,
                'error': 'Non-existent hint!'}
    hints.update(hintspec, {'$inc': {'votes': 1}})

    # Return a list of how many votes each hint has now.
    vote_counts = []    # [hint, id, votes] sublists
    for hint_id in matching_user['hints_shown']:
        hint = hints.find_one({'_id': hint_id})
        if hint is None:
            # Hint no longer exists - just go on.
            continue
        vote_counts.append([hint['hint'], str(hint_id), hint['votes']])

    # Clear the user's history, and don't let him vote again.
    userdata.update(spec, {'$set': {
        'hints_shown': [],
        'previous_answers': [],
    }})
    settings = mongodb['settings']
    if not settings.find_one({'location': location})['debug']:
        userdata.update(spec, {'$set': {'voted': True}})
    return {'success': True,
            'vote_counts': vote_counts}


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
    # Find the user-problem pair.
    in_dict = json.loads(in_dict_json)
    location = in_dict['location']
    answer = in_dict['answer']
    userdata = mongodb['userdata']
    spec = {
        'user': in_dict['user'],
        'location': location,
    }
    problem_settings = mongodb['settings'].find_one({'location': location})

    # This is a temporary instructor bypass, until I figure out how authentication
    # on edInsights works.
    if in_dict['user'] != 'instructor':
        # Make sure the user is actually qualified to submit a hint.
        matching_user = userdata.find_one(spec)
        if matching_user['voted']:
            return {'success': False,
                    'error': 'Already voted!'}

        if problem_settings is None or problem_settings['display_only']:
            return {'success': False,
                    'error': 'This problem does not accept hints!'}

    if query.validate_answer(json.dumps(location), answer) != 'true':
        return {'success': False,
                'error': 'Invalid answer!'}

    # Now, add the hint to the database.
    hints = mongodb['hints']
    hints.insert({
        'location': location,
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
    return {'success': True}


@query()
def list_problems(mongodb, query, in_dict_json):
    """
    Returns all problems that have hinting in this course.
    in_dict has one entry: 'course', which specifies the
    course, in org/code/name form.
    Returns a list of [location, name] pairs.
    """
    in_dict = json.loads(in_dict_json)
    location_chunks = in_dict['course'].split('/')
    settings = mongodb['settings']
    matches = settings.find({'location': {'$all': location_chunks[:2]}})
    out = []
    for problem in matches:
        name = query.get_name(json.dumps(problem['location']))
        out.append([problem['location'], name])
    return {'success': True,
            'problems': out}

@query()
def dump_hints(mongodb, query, in_dict_json):
    """
    Returns hints for the problem specified by 'location' in in_dict.
    Filters by the 'field' in in_dict, to display either problems
    in the 'mod_queue' or approved 'hints'
    """
    in_dict = json.loads(in_dict_json)
    location = in_dict['location']
    if in_dict['field'] == 'mod_queue':
        approved = False
    else:
        approved = True
    dumped_hints = mongodb['hints'].find({
        'location': location,
        'settings.approved': approved,
    })

    # Make a list of [id, answer, hint text, votes] for each hint.
    hint_list = []
    for hint in dumped_hints:
        hint_list.append([str(hint['_id']), hint['answer'], hint['hint'], hint['votes']])
    return {'success': True,
            'hints': hint_list,
            'problem_name': query.get_name(json.dumps(location))}


@query()
def delete_hints(mongodb, query, in_dict_json):
    """
    Deletes hints, for instructors.
    in_dict is expected to have key 'to_delete', corresponding to a list of
    id's to delete.
    """
    to_delete = json.loads(in_dict_json)['to_delete']
    hints = mongodb['hints']
    for hint_id in to_delete:
        hints.remove({'_id': ObjectId(hint_id)})
    return {'success': True}


@query()
def change_votes(mongodb, query, in_dict_json):
    """
    Changes vote counts, for instructors.
    in_dict is expected to have key 'updated_votes'.
    in_dict['updated_votes'] is a list containing sublists of
    [pk, new_votes], each of which representing a hint and the
    new vote count.
    """
    updated_votes = json.loads(in_dict_json)['updated_votes']
    hints = mongodb['hints']
    for hint_id, new_votes in updated_votes:
        hints.update({'_id': ObjectId(hint_id)},
                     {'$set': {'votes': int(new_votes)}})
    return {'success': True}


@query()
def approve_hints(mongodb, query, in_dict_json):
    """
    Approves hints, for instructors.
    in_dict is expected to have key 'to_approve'
    in_dict['to_approve'] is a list of pk's of hints to approve.
    """
    to_approve = json.loads(in_dict_json)['to_approve']
    hints = mongodb['hints']
    for hint_id in to_approve:
        hints.update({'_id': ObjectId(hint_id)},
                     {'$set': {'settings.approved': True}})
    return {'success': True}


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
