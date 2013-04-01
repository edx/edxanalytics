from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url('^', include('djanalytics.core.urls')),

    url(r'^httpevent$', 'djeventstream.httphandler.views.http_view'),
    url(r'^snsevent$', 'djeventstream.snshandler.views.sns_view'),

    url('^tasks/', include('djcelery.urls')),

    url(r'^$', 'dashboard.views.new_dashboard'),
    url(r'^dashboard$', 'dashboard.views.dashboard'),
    url(r'^new_dashboard$', 'dashboard.views.new_dashboard'),
    url(r'^frontend/', include('frontend.urls')),
    # Examples:
    # url(r'^$', 'edxanalytics.views.home', name='home'),
    # url(r'^edxanalytics/', include('edxanalytics.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

## TODO: Code review of below patterns and protected_data
if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
    urlpatterns+= patterns('',
                           url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                               'document_root': settings.STATIC_ROOT,
                               'show_indexes' : True,
                               }),
                           url(r'^data/(?P<path>.*)$', 'django.views.static.serve', {
                               'document_root': settings.PROTECTED_DATA_ROOT,
                               'show_indexes' : True,
                               }),
                           )
else:
    urlpatterns+= patterns('frontend.views',
                           url(r'^data/(?P<path>.*)$', 'protected_data')
    )

## TODO: Confirm these work with new settings.py, confirm they're
## helpful
handler404 = 'error_templates.render_404'
handler500 = 'error_templates.render_500'
