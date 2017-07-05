
from django.contrib import admin
from .models import *


@admin.register(Satellite)
class SatelliteAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "longi", "lati", "alti", "date")

@admin.register(SatHistory)
class SatHistoryAdmin(admin.ModelAdmin):
    list_display = ("name", "longi", "lati", "alti", "date")
