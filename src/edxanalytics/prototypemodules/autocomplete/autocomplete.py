from edinsights.core.decorators import query

@query()
def autocomplete_available():
    ''' Returns a list of parameters for which the system has an
    autocomplete. '''
    return ['user']

@query()
def autocomplete(parameter, start):
    return ['pmitros', 'piotr', 'peter']
