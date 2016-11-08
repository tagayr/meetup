from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.http import Http404
from django.views import generic
from .forms import EventForm, ParticipantForm, JoinEventForm, ParticipantReducedForm

from .models import Event, GatheringLocation, Address

# Create your views here.


def index(request):
    context = {}
    return render(request, "meetup/index.html", context)


class DetailView(generic.DetailView):
    model = Event
    template_name = "meetup/detail.html"


def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # assign a random key to the event
            event.generate_key()
            # print("=======================" + event.event_key)
            event = form.save()
            event_id = event.id
            return HttpResponseRedirect(reverse("meetup:detail", args=(event_id,)))
            # return HttpResponseRedirect(reverse("meetup:index",))

    else:
        form = EventForm()

    return render(request, 'meetup/new_event.html', {'form': form})


def new_participant(request, event_id):
    # this view is DEPRECATED
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        # print('==========================' + event_id)
        participant_form = ParticipantForm(request.POST)

        # check validity of participant -- <form action="{% url 'meetup:new_participant' event_id %}" method="post">
        if participant_form.is_valid():
            participant = participant_form.save(commit=False)
            participant.event = event
            participant.save()

            # create new address object
            # better to do that in a method in models.py
            '''
            address = Address(event=event, street_name=participant.street_name, city=participant.city,
                              postal_code=participant.postal_code, country=participant.country,
                              address_type="PA")
            address.get_lat_long()
            address.save()
            '''
            participant.set_address()
            return HttpResponseRedirect(reverse("meetup:detail", args=(event_id,)))

    else:
        participant_form = ParticipantForm()
        context = {
           'participant_form': participant_form
        }
        return render(request, "meetup/new_participant.html", context)


def new_participant2(request, event_id):
    # new attempt with one single address bar
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        participant_form = ParticipantReducedForm(request.POST)

        if participant_form.is_valid():
            participant = participant_form.save(commit=False)
            participant.event = event
            address_google = request.POST.get("googleaddress", "")
            participant.full_address = address_google
            participant.save()
            participant.set_address()

            return HttpResponseRedirect(reverse("meetup:detail", args=(event_id,)))

    else:
        participant_form = ParticipantForm()
        context = {
           'participant_form': participant_form
        }
        return render(request, "meetup/new_participant2.html", context)


def join_event(request):
    if request.method == 'POST':
        join_event_form = JoinEventForm(request.POST)
        if join_event_form.is_valid():
            # event_key = join_event_form.fields['event_key']
            instance = join_event_form.save(commit=False)
            event_key = instance.event_key
            print('=================' + event_key)
            # to be potentially enhanced
            event = get_object_or_404(Event, event_key=event_key)
            event_id = event.id
            return HttpResponseRedirect(reverse("meetup:detail", args=(event_id,)))

    else:
        join_event_form = JoinEventForm()
        context = {
            'join_event_form': join_event_form
        }
        return render(request, "meetup/join.html", context)


def locations(request, event_id):
    event = Event.objects.get(pk=event_id)

    # currently running on fixed lat and long
    # insert here a function to generate central lat and long

    # set the gathering locations
    event.set_gathering_locations()
    # get the gathering locations to pass them in to the template
    gathering_locations = GatheringLocation.objects.filter(event=event_id)
    context = {
        'gathering_locations': gathering_locations
    }
    return render(request, 'meetup/locations.html', context)


'''
class LocationsListView(generic.ListView):
    template_name = "meetup/locations.html"
    context_object_name = 'gathering_locations'

    def get_queryset(self):
        return GatheringLocation.objects.all()

'''
