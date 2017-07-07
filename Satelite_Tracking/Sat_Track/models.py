from django.db import models
from django_countries.fields import CountryField


class SpaceAgency(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa')
    acronym = models.CharField(max_length=128, verbose_name='Akronim')
    country = CountryField(verbose_name='Państwo')
    launch_capable = models.BooleanField(default=False, verbose_name='Może wystrzelić satelitę')

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


class Astronaut(models.Model):
    first_name = models.CharField(max_length=128, verbose_name='Imię')
    last_name = models.CharField(max_length=128, verbose_name='Nazwisko')
    agency = models.ForeignKey(SpaceAgency, verbose_name='Agencja')
    satellite = models.ForeignKey(Satellite, verbose_name='Obiekt')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)














