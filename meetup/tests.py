from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Event, Participant, ParticipantAddress, GatheringLocation

# Create your tests here.


class EventMethodTest(TestCase):
    def test_was_created_recently_with_future_event(self):
        """
        was_created_recently should return false for events that are published in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_event = Event(created_on=time)
        self.AssertEqual(future_event.was_created_recently(), False)

    def test_was_created_recently_with_past_event(self):
        """
        was_created_recently should return false for events older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=2)
        past_event = Event(created_on=time)
        self.AssertEqual(past_event.was_created_recently(), False)

    def test_was_created_recently_with_recent_event(self):
        """
        was_created_recently should return true for events older than 1 day
        """
        time = timezone.now() - datetime.timedelta(hours=2)
        recent_event = Event(created_on=time)
        self.AssertEqual(recent_event.was_created_recently(), False)

    def test_created_on_returns_current_datetime(self):
        """
        created_on attribute should return the datetime at which the instance was created
        """
        new_event = Event()
        time = timezone.now
        delta = new_event.created_on - time
        check_delta = delta < datetime.timedelta(seconds=1)
        self.AssertEqual(check_delta, True)


# class ParticipantMethodTest(TestCase):

# class ParticipantAddressMethodTest(TestCase):

# class GatheringLocationMethodTest(TestCase):