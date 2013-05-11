from djanalytics.core.decorators import query, event_handler

@query()
def user_autocomplete(user):
    ''' Returns all the users in the system
    '''
    return list(User.objects.using(database='lms').filter( username__startswith =user ).limit(20))



@query()
def course_list():
    CourseEnrollment.objects.using(database='lms').all().values('course_id').distinct()
