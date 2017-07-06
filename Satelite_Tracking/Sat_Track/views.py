from django.http import HttpResponse
from django.shortcuts import render
from django.views import *
from django.views.generic.edit import *

from .models import *


import kronos

import json
# from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from django.core.exceptions import ObjectDoesNotExist

from pyorbital.orbital import Orbital
from datetime import datetime
""" Not working for now:
'CloudSat',
'CryoSat 2',
'CSK 1',
'CSK 2',
'CSK 3',
'CSK 4',
'DMSP F15',
'DMSP F16',
'DMSP F17',
'DMSP F18',
'DMSP F19',
'EOS Aqua',
'EOS Aura',
'EOS Terra',
'FY 2D',
'FY 2E',
'FY 2F',
'FY 2G',
'FY 3A',
'FY 3B',
'FY 3C',
'GOES 13',
'GOES 14',
'GOES 15',
'Himawari 6',
'Himawari 7',
'Himawari 8',
'INSAT 3A',
'INSAT 3C',
'INSAT 3D',
'JASON 2',
'Kalpana 1',
"""


SAT_NAME = [
'ALOS-2',
'Landsat 7',
'Landsat 8',
'Meteosat 7',
'Meteosat 8',
'Meteosat 9',
'Meteosat 10',
'Metop A',
'Metop B',
'NOAA 15',
'NOAA 16',
'NOAA 17',
'NOAA 18',
'NOAA 19',
'RadarSat 2',
'Sentinel 1A',
'SMOS',
'SPOT 5',
'SPOT 6',
'SPOT 7',
'Suomi NPP',
'TanDEM X',
'TerraSAR X',
]


# manage.py installtasks
# You can review the crontab with a crontab -l command
@kronos.register('* * * * *')
def actuate_sats():
    for name in SAT_NAME:
        try:
            orb = Orbital(name)
            now = datetime.utcnow()
            # Get normalized position and velocity of the satellite:
            # normal_position = orb.get_position(now)
            # Get longitude, latitude and altitude of the satellite:
            geo_position = orb.get_lonlatalt(now)
            print("Found {} - {}".format(name, geo_position))
            try:
                if Satellite.objects.get(name=name):
                    # if there is satellite with such name -> update info
                    sat = Satellite.objects.get(name=name)
                    # save past position
                    sat_hist = SatHistory.objects.create(name=sat.name,
                                                         longi=sat.longi,
                                                         lati=sat.lati,
                                                         alti=sat.alti)
                    sat_hist.save()
                    # update to actual position
                    sat.longi = geo_position[0]
                    sat.lati = geo_position[1]
                    sat.alti = geo_position[2]
                    sat.date = datetime.utcnow()
                    sat.save()
                    sat.hist = SatHistory.objects.filter(name=name)
                    sat.save()

            except ObjectDoesNotExist:
                # if there is no satellite with such name
                # creating is possible
                sat = Satellite.objects.create(name=name,
                                               longi=geo_position[0],
                                               lati=geo_position[1],
                                               alti=geo_position[2]
                                               )
                sat.save()

        except (KeyError, NotImplementedError):
            print('No satellite name: {}'.format(name))


class Map(View):
    # pass
    def get(self, request):
        # satellites = Satellite.objects.get(pk=11)
        # satellites = Satellite.objects.filter(pk__in=[11, 13])
        satellites = Satellite.objects.all()
        # sats_json = serializers.serialize('json',
        # Satellite.objects.filter(pk__in=[11, 13]))
        sats_json = serializers.serialize('json', Satellite.objects.all())
        # get id of history objects related to satellite
        hist_id = []
        for sat in satellites:
            hist_list_id = sat.hist.all()
            for hist in hist_list_id:
                hist_id.append(hist.id)

        sats_hist_json = serializers.serialize('json',
                         SatHistory.objects.filter(pk__in=hist_id))

        context = {
            "satellites": satellites,
            "sats_json": sats_json,
            "sats_hist_json": sats_hist_json,
        }
        return render(request, "map.html", context)


class Satellites(View):
    def get(self, request):
        # actuate_sats()
        satellites = Satellite.objects.all()
        context = {
            "satellites": satellites
        }
        return render(request, "satellites.html", context)


class SatellitesInfo(View):

    def get(self, request, sat_id):
        satellite = Satellite.objects.get(pk=sat_id)
        sat_history = SatHistory.objects.filter(name=
                                                satellite.name).order_by('-date')
        astronauts = satellite.astronaut_set.all()
        agency = satellite.agency
        context = {
            "satellite": satellite,
            "history": sat_history,
            "astronauts": astronauts,
            "agency": agency,
        }
        return render(request, "satellite_info.html", context)




class UpdateSatellites(UpdateView):
    model = Satellite
    template_name = "satellites_update_form.html"
    fields = ['agency']
    success_url = '/satellites'


class SpaceAgencies(View):
    def get(self, request):
        # actuate_sats()
        agencies = SpaceAgency.objects.all()
        context = {
            "agencies": agencies
        }
        return render(request, "agencies.html", context)


class AgencyInfo(View):

    def get(self, request, agency_id):
        agency = SpaceAgency.objects.get(pk=agency_id)
        satellites = agency.satellite_set.all()
        astronauts = agency.astronaut_set.all()
        # sat_history.sort(key=operator.itemgetter('date'))
        context = {
            "agency": agency,
            "satellites": satellites,
            "astronauts": astronauts,
        }
        return render(request, "agency_info.html", context)


class AddSpaceAgency(CreateView):
    model = SpaceAgency
    template_name = "add_space_agency_form.html"
    fields = ['name', 'acronym', 'country', 'launch_capable']
    success_url = '/space_agencies'


class UpdateSpaceAgency(UpdateView):
    model = SpaceAgency
    template_name = "spaceagency_update_form.html"
    fields = ['name', 'acronym', "country", "launch_capable"]
    success_url = '/space_agencies'


class DeleteSpaceAgency(DeleteView):
    model = SpaceAgency
    template_name = "spaceagency_confirm_delete.html"
    success_url = '/space_agencies'


class Astronauts(View):
    def get(self, request):
        # actuate_sats()
        astronauts = Astronaut.objects.all()
        context = {
            "astronauts": astronauts,
        }
        return render(request, "astronauts.html", context)


class AstronautsInfo(View):

    def get(self, request, astr_id):
        astronaut = Astronaut.objects.get(pk=astr_id)
        agency = astronaut.agency
        satellite = astronaut.satellite
        context = {
            "astronaut": astronaut,
            "satellite": satellite,
            "agency": agency,
        }
        return render(request, "astronauts_info.html", context)


class AddAstronauts(CreateView):
    model = Astronaut
    template_name = "add_astronauts_form.html"
    fields = ['first_name', 'last_name', 'agency', 'satellite']
    success_url = '/astronauts'


class UpdateAstronauts(UpdateView):
    model = Astronaut
    template_name = "astronauts_update_form.html"
    fields = ['first_name', 'last_name', "agency", "satellite"]
    success_url = '/astronauts'


class DeleteAstronauts(DeleteView):
    model = Astronaut
    template_name = "astronauts_confirm_delete.html"
    success_url = '/astronauts'














