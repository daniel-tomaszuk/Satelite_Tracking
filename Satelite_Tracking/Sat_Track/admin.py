
from django.contrib import admin
from .models import *


@admin.register(Satellite)
class SatelliteAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "longi", "lati", "alti", "date")


@admin.register(SatHistory)
class SatHistoryAdmin(admin.ModelAdmin):
    list_display = ("name", "longi", "lati", "alti", "date")


@admin.register(SpaceAgency)
class SatHistoryAdmin(admin.ModelAdmin):
    list_display = ("name", "acronym", "country", "launch_capable")


@admin.register(Astronaut)
class SatHistoryAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "satellite", "agency")

