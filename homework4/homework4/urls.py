from django.conf.urls import patterns, include,url
from django.conf import settings
from django.contrib import admin 
admin.autodiscover() 

# Default URL routes file for the controller.  Here we are simply matching
# URL patterns by regular expression, and choosing the actual route by
# including the appropriate route file for each application.
urlpatterns = patterns('',
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)), 
)
