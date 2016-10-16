from django.contrib import admin

from .models import Event, Participant, GatheringLocation, Address

# Register your models here.
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(GatheringLocation)
admin.site.register(Address)
