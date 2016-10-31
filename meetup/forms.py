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

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields["participant_name"].required = True
        self.fields["participant_email"].required = True
        self.fields["street_name"].required = True
        self.fields["postal_code"].required = True
        self.fields["city"].required = True

        # self.fields["participant_name"].help_text = "Please enter your name."


class JoinEventForm(ModelForm):

    class Meta:
        model = Event
        fields = ['event_key']
