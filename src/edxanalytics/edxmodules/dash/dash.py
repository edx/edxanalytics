import inspect

from edinsights.core.decorators import view

@view()
def selector_dash(view, analytic):
    ''' Wrapper around a single analytic to make it global, and ask
    the user for the relevant parameters.
    '''
    from edinsights.core.render import render
    f = view.__getattr__(analytic)
    params = inspect.getargspec(f).args 
    return render("single_dash.html", {'parameters' : params, 
                                       'analytic' : analytic})

@view()
def dash(view):
    ''' Show a list of analytics, wrapped in selector_dash '''
    from edinsights.core.render import render
    analytics = view.__dir__()
    return render("full_dash.html", {'analytics' : analytics})
