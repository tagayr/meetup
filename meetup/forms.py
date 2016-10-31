from django.forms import ModelForm
from django import forms
from meetup.models import Event, Participant


# Create your forms here


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_type', 'event_datetime']


class ParticipantForm(ModelForm):
    """
    def __init__(self, *args, **kwargs):
        self._event = kwargs.pop('event')
        super(ParticipantForm, self).__init__(*args, **kwargs)
    """
    class Meta:
        model = Participant
        fields = ['participant_name', 'participant_email', 'street_name', 'postal_code', 'city',
                  'country']


class JoinEventForm(ModelForm):

    class Meta:
        model = Event
        fields = ['event_key']
