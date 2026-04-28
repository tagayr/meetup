from django.urls import re_path

from . import views

app_name = 'meetup'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^new_event/$', views.new_event, name='new_event'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^(?P<event_id>[0-9]+)/new_participant/$', views.new_participant, name='new_participant'),
    re_path(r'^(?P<event_id>[0-9]+)/new_participant2/$', views.new_participant2, name='new_participant2'),
    re_path(r'^join/$', views.join_event, name="join_event"),
    re_path(r'^(?P<event_id>[0-9]+)/locations/$', views.locations, name="gathering_locations"),
]
