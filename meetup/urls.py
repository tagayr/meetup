from django.conf.urls import url

from . import views

app_name = 'meetup'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_event/$', views.new_event, name='new_event'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<event_id>[0-9]+)/new_participant/$', views.new_participant, name='new_participant'),
    url(r'^(?P<event_id>[0-9]+)/new_participant2/$', views.new_participant2, name='new_participant2'),
    url(r'^join/$', views.join_event, name="join_event"),
    # url(r'^(?P<event_id>[0-9]+)/locations/$', views.LocationsListView.as_view(), name="gathering_locations"),
    url(r'^(?P<event_id>[0-9]+)/locations/$', views.locations, name="gathering_locations"),
]
