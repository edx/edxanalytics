from django.conf.urls import patterns, include, url

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
