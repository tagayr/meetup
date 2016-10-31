from django.db import models
import datetime
from django.utils import timezone
import random
import string
import requests
import json


# Create your models here.


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_key = models.CharField(max_length=50, null=True)
    created_on = models.DateTimeField(default=timezone.now())
    # How do i insert a binary selection
    EAT = 'E'
    DRINK = 'D'
    EVENT_TYPES = (
        (EAT, 'Eat'),
        (DRINK, 'Drink'),
    )
    event_type = models.CharField(
        max_length=2,
        choices=EVENT_TYPES,
        default=DRINK,
    )
    event_datetime = models.DateTimeField(default=timezone.now() + datetime.timedelta(hours=2))
    event_url_link = models.URLField(default="/meetup/index.html")

    def __str__(self):
        return self.event_name

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_on <= now

    def generate_key(self, size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        random_key = ''.join(random.choice(chars) for _ in range(size))
        self.event_key = random_key

    # basic centroid calculation method
    def get_centroid(self):
        sum_lat = 0
        sum_long = 0
        participant_addresses = Address.objects.filter(event=self)
        for address in participant_addresses:
            sum_lat += address.latitude
            sum_long += address.longitude

        centroid_lat = sum_lat / participant_addresses.__len__()
        centroid_long = sum_long / participant_addresses.__len__()

        centroid = {'lat': centroid_lat,
                    'long': centroid_long}

        print("================ lat", centroid["lat"])
        print("================ long", centroid["long"])

        return centroid

    # insert a more elaborate centroid calculation method here !

    def get_gathering_locations(self):

        # there should be here a call to a function to get the lat and long of the central location
        # for all attendees

        # lat = -33.8670522
        # long = 151.1957362

        centroid = self.get_centroid()
        # event_type = ""
        if self.event_type == "Drink":
            event_types = 'bar|cafe'  # night_club
            keyword = "bar_beer_wine_cocktail"
        else:
            event_types = 'food|restaurant'
            keyword = "restaurant+marocain+couscous+libanais+sushi+japonais+brunch+burger"

        # radius is 500 by default
        radius = 1000
        lat = centroid['lat']
        long = centroid['long']

        # nearby search

        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(long) + \
              "&radius=" + str(radius) + "&types=" + event_types + \
              "&rankby=prominence&key=AIzaSyApI6kqh3c2bsxUuejRh7dNwRBDKyw0mxA"

        # url backup without keyword
        '''
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(long) + \
              "&radius=" + str(
            radius) + "&types=" + event_types + "&name=cruise&key=AIzaSyApI6kqh3c2bsxUuejRh7dNwRBDKyw0mxA"
        '''

        r = requests.get(url)  # get or post
        response = r.json()
        locations = response['results']
        return locations

    def delete_previous_gathering_locations(self):
        gathering_locations = GatheringLocation.objects.filter(event=self.id)
        for location in gathering_locations:
            location.delete()

    def set_gathering_locations(self):
        # first delete old locations
        self.delete_previous_gathering_locations()

        # then generate new ones
        locations = self.get_gathering_locations()

        # finally, populate the database
        for location in locations:
            name = location['name']
            address = location['vicinity']
            location = GatheringLocation(event=self, location_name=name, location_address=address)
            location.get_href()
            location.save()


class Participant(models.Model):
    event = models.ForeignKey(Event, primary_key=False, on_delete=models.CASCADE)  # used to have to have no pk

    # Participant details
    participant_name = models.CharField(max_length=50, null=True)
    participant_email = models.EmailField(default="john@doe.com")
    # participant_message = models.CharField(max_length=200, default='')

    # Participant address details
    # street_number = models.IntegerField(default=1)
    street_name = models.CharField(max_length=200, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, default='France')

    # latitude and longitude are probably not needed for participant
    latitude = models.DecimalField(default=0.0, max_digits=20, decimal_places=17)
    longitude = models.DecimalField(default=0.0, max_digits=20, decimal_places=17)

    def __str__(self):
        return self.participant_name

    def participant_address(self):
        return "{} - {} {}".format(self.street_name, self.postal_code, self.city)

    def set_address(self):
        address = Address(event=self.event, street_name=self.street_name, city=self.city,
                          postal_code=self.postal_code, country=self.country,
                          address_type="PA")

        address.get_lat_long()
        address.save()


class GatheringLocation(models.Model):
    event = models.ForeignKey(Event, primary_key=False, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=200, null=True)
    location_address = models.CharField(max_length=500, null=True)
    href = models.CharField(max_length=200, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.location_name

    def get_href(self):
        query = self.location_name.replace(" ", "+") + "+" + self.location_address.replace(" ", "+")
        self.href = "http://www.google.com/search?q=" + query


class Address(models.Model):
    event = models.ForeignKey(Event, primary_key=False, on_delete=models.CASCADE, null=True)
    street_name = models.CharField(max_length=200, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, default='France')

    latitude = models.DecimalField(default=0.0, max_digits=20, decimal_places=17)
    longitude = models.DecimalField(default=0.0, max_digits=20, decimal_places=17)

    PARTICIPANT_ADDRESS = "PA"
    GATHERING_LOCATION_ADDRESS = "GLA"

    ADDRESS_TYPES = (
        (PARTICIPANT_ADDRESS, "Participant address"),
        (GATHERING_LOCATION_ADDRESS, "Gathering location address")
    )

    address_type = models.CharField(max_length=3, choices=ADDRESS_TYPES, default=GATHERING_LOCATION_ADDRESS)

    def __str__(self):
        return "{} - {} {}".format(self.street_name, self.postal_code, self.city)

    # get address latitude and longitude

    # api call:  https://maps.googleapis.com/maps/api/geocode/json?address=
    # 1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyDcddwoJvWCirP_S9GjbCIVu5V8OjtKMRM

    def geolocate(self):
        address_in_url = self.street_name + "+" + self.postal_code + "+" + self.city + "+" + self.country
        address_in_url.replace(' ', '+')
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address_in_url \
              + "&key=AIzaSyDcddwoJvWCirP_S9GjbCIVu5V8OjtKMRM"

        r = requests.get(url)  # get or post
        response = r.json()
        lat_lng = response['results'][0]['geometry']['location']
        return lat_lng

    def get_lat_long(self):
        lat_lng = self.geolocate()
        self.latitude = lat_lng['lat']
        self.longitude = lat_lng['lng']
