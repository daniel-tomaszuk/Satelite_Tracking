from django.db import models

# Create your models here.


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

    def __str__(self):
        return "{}".format(self.name)







