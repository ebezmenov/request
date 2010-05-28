from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns
from hcb.gin.views import archive

urlpatterns = patterns('',
    url(r'^$', archive),
)