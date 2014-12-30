from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from reports import views

urlpatterns = patterns('',
                       url(r'^$', login_required(views.dashboard), name='index'),
                       url(r'^(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.report, name='report'),
                       url(r'^(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/graph/?$', views.graph, name='graph'),
                       url(r'^(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/screenshot/?$', views.screenshot, name='screenshot'),
                       url(r'^(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/pcap/?$', views.pcap, name='pcap'),
                       url(r'^login$','django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       url(r'^logout$','django.contrib.auth.views.logout_then_login')
                   
)
