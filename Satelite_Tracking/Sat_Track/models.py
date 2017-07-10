from django.db import models
from django_countries.fields import CountryField


class SpaceAgency(models.Model):
    name = models.CharField(max_length=128, verbose_name='Name')
    acronym = models.CharField(max_length=128, verbose_name='Acronym')
    country = CountryField(verbose_name='Country')
    launch_capable = models.BooleanField(default=False,
                                         verbose_name='Launch Capable')

    def __str__(self):
        return "{}".format(self.name)


class SatHistory(models.Model):
    name = models.CharField(max_length=128, default=None)
    date = models.DateTimeField(auto_now=True)
    longi = models.FloatField()
    lati = models.FloatField()
    alti = models.FloatField()

    def __str__(self):
        return "{} {}".format(self.name, self.date)


class Satellite(models.Model):
    # norad_id = models.IntegerField()
    name = models.CharField(max_length=128)
    # Get longitude, latitude and altitude of the satellite
    longi = models.FloatField()
    lati = models.FloatField()
    alti = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    hist = models.ManyToManyField(SatHistory)
    # date = models.CharField(max_length=64)
    agency = models.ForeignKey(SpaceAgency, null=True)

    def __str__(self):
        return "{}".format(self.name)


class Personnel(models.Model):
    first_name = models.CharField(max_length=128, verbose_name='First Name')
    last_name = models.CharField(max_length=128, verbose_name='Last Name')
    agency = models.ForeignKey(SpaceAgency, null=True,
                               verbose_name='Space Agency')
    satellite = models.ForeignKey(Satellite, null=True, verbose_name='Object')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

