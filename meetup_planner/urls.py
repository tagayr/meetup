from django.urls import re_path, include
from django.contrib import admin

urlpatterns = [
    re_path(r'^polls/', include('polls.urls')),
    re_path(r'^meetup/', include('meetup.urls')),
    re_path(r'^admin/', admin.site.urls),
]
