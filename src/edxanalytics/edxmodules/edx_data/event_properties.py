### This is the start of a module for bringing high-level information
### out of events (along the lines of Tincan). This code is untested,
### so this module should not be included in settings.py without
### further testing.

from djanalytics.core.decorators import event_property

@event_property(name="agent")
def agent(event):
    ''' Returns the user that generated the event. The terminology of
    'agent' is borrowed from the Tincan agent/verb/object model. '''
    if "user" in event:
        return event["user"]
    elif "username" in event:
        return event["username"]
    else:
        return None

@event_property(name="university")
def university(event):
    ''' Returns the university associated with a given event. 
    Will return:
      'unknown' where this is not known (e.g calculator, or new events). 
      'Global' is edX-global (e.g. registration pages)
    '''
    try:
        event = json.loads(item)
        if event['event_source'] == 'server': ## Middleware item
            evt_type = event['event_type']
            if '/courses/' in evt_type: ## Middleware item in course
                institution = evt_type.split('/')[2]
                return institution
            elif '/' in evt_type: ## Middle ware item not in course
                return "Global"
            else:  ## Specific server logging. One-off parser for each type
                #Survey of logs showed 4 event types: reset_problem
                #save_problem_check, save_problem_check_fail, save_problem_fail
                # All four of these have a problem_id, which we
                # extract from
                try: 
                    return event['event']['problem_id'].split('/')[2]
                except: 
                    return "Unknown"
        elif event['event_source'] == 'browser': # Caught in browser
            page = event['page']
            if 'courses' in page:
                institution = page.split('/')[4]
                return institution
            else: 
                ## Code path unchecked/non-course has no 
                ## instrumentation
                return "Unknown"
    except:
        return "Unknown"
