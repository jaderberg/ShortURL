from django.conf.urls.defaults import patterns, include, url, handler404

handler404 = 'django.views.defaults.page_not_found()'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'shortner.views.index'),
    url(r'^((?!check_code))((?!get_code))((?!admin))((?!delete))(?P<code>.+)/$', 'shortner.views.code_redirect'),
    url(r'^get_code/(?P<url>.+)', 'shortner.views.get_code'),
    url(r'^delete_code/(?P<code>.+)/$', 'shortner.views.delete_code'),
    url(r'^check_code/(?P<code>.+)/$', 'shortner.views.check_code'),
    url(r'^admin/', include(admin.site.urls)),
)
