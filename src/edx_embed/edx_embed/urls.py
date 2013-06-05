from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^djdash/', 'djembed.views.proxy', name='proxy'),
    url(r'^sysadmin_dash/$', 'djembed.views.sysadmin_dash', name='proxy'),
    url(r'^$', 'djembed.views.home', name='home'),
    # url(r'^edx_embed/', include('edx_embed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
