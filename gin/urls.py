from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.contrib.auth.views import logout, login
from hcb.gin.models import Incident
#from hcb.gin.views import archive

urlpatterns = patterns('hcb.gin.views',
    url(r'^$', 'index', name = 'list_inc'),
    url(r'^archive/$', 'archive'),
    url(r'^list/$',object_list,{'queryset':Incident.objects.all(), 'template_name':'index.html'}),
    url(r'incident/(\d+)/$','incident_detail_view',name='incident_detail'),
    url(r'incident/(\d+)/edit$','incident_detail',name='incident_view'),
    url(r'new/$','new_incident', name='new_incident'),
)
info_dic = {'queryset': Incident.objects.all(), 'template_name':'list.html'}
create_info = {'model': Incident}
urlpatterns +=patterns('django.views.generic',
    url(r'list2/$', 'list_detail.object_list',info_dic, name='list2'),
    url(r'^add_req/$','create_update.create_object', create_info, name='add_inc'),
)