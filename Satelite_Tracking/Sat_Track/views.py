from django.http import HttpResponse
from django.shortcuts import render
from django.views import *
from django.views.generic.edit import *
from .models import *
import kronos

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

# import json
# from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from pyorbital.orbital import Orbital
from datetime import datetime

SAT_NAME = [
            'ALOS-2', 'Landsat 7', 'Landsat 8', 'Meteosat 7', 'Meteosat 8',
            'Meteosat 9', 'Meteosat 10', 'Metop A', 'Metop B', 'NOAA 15',
            'NOAA 16', 'NOAA 17', 'NOAA 18', 'NOAA 19', 'RadarSat 2',
            'Sentinel 1A', 'SMOS', 'SPOT 5', 'SPOT 6', 'SPOT 7', 'Suomi NPP',
            'TanDEM X', 'TerraSAR X',
            ]


# ./manage.py installtasks -> to run kronos
# You can review the crontab with a crontab -l command
@kronos.register('* * * * *')  # every minute
def actuate_sats():
    """
    Use external library to get positions of requested satellites.
    Create new Satellite (look at models) object if there is no satellite with
    found name, or update existing satellite if it's already in the DB
    :return: None - only create/update/do nothing on DB objects
    """
    for name in SAT_NAME:
        try:
            orb = Orbital(name)
            now = datetime.utcnow()
            # Get longitude, latitude and altitude of the satellite
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
        # if there is no satellite with such name in sources
        except (KeyError, NotImplementedError):
            print('No satellite name found in the sources: {}'.format(name))


class Map(View):

    def get(self, request):
        # on get - show map without satellites
        context = {
            "satellites": "",
            "sats_json": "{}",
            "sats_hist_json": "{}",
        }
        return render(request, "map.html", context)

    def post(self, request):
        sat_list = []
        # date selected in satellite display form (url: sat-all, Satellites")
        the_date = request.POST.get('the_date')
        for sat_name in SAT_NAME:
            name = request.POST.get(sat_name)
            if name:
                sat_list.append(name)
        # get chosen satellites (from satellites template)
        satellites = Satellite.objects.filter(name__in=sat_list)
        # make json out of chosen satellites
        sats_json = serializers.serialize('json', satellites)
        # get id of history objects related to satellite
        hist_id = []
        # for every chosen satellite
        for sat in satellites:
            # take every history instance (for given satellite) id
            hist_list = sat.hist.all()
            for hist in hist_list:
                if hist.date.date().isoformat() == the_date:
                    hist_id.append(hist.id)

        # make json out of history instances
        sats_hist_json = serializers.serialize('json',
                         SatHistory.objects.filter(pk__in=hist_id))

        context = {
            "satellites": satellites,
            "sats_json": sats_json,
            "sats_hist_json": sats_hist_json,
        }
        return render(request, "map.html", context)


class SatellitesList(APIView):

    def get_object(self, name_list):
        """
        Gets most recent points with satellite NAME = name from DB
        :param name: name of satellite which history to get
        :return: all present points of satellite with name = slug
        """
        try:
            # names selected in satellites.html template form
            # (url: sat-all, Satellites")
            return Satellite.objects.filter(name__in=name_list)

        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, format=None):
        """
        Serializes and returns all satellites in DB
        :param request: http request
        :param format:
        :return: Serializes data selected by GET parameters
        """

        sat_list = []
        for sat_name in SAT_NAME:
            # names selected in satellites.html template form
            name = request.GET.get(sat_name)
            if name:
                sat_list.append(name)

        present = self.get_object(sat_list)
        serializer = SatelliteSerializer(present, many=True,
                                         context={"request": request})
        return Response(serializer.data)


class History(APIView):

    def get_object(self, name, isodate):
        """
        Gets history with satellite NAME = name from DB
        :param name: name of satellite which history to get
        :return: all history (past positions) of satellite with name = slug
        """
        try:
            # date selected in satellite display form
            # (url: sat-all, Satellites")
            return SatHistory.objects.filter(name__in=name)\
                                     .filter(date__contains=isodate)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, format=None):
        """
        Gets, serializes and returns SatHistory object with  name = sat_name
        :param request: http request
        :param name: name of satellite which history to get
        :param format: None
        :return: serialized SatHistory data
        """
        sat_list = []
        for sat_name in SAT_NAME:
                name = request.GET.get(sat_name)
                if name:
                    sat_list.append(name)

        isodate = request.GET.get('the_date')
        history = self.get_object(sat_list, isodate)
        serializer = SatHistorySerializer(history, many=True,
                                          context={"request": request})
        return Response(serializer.data)


class Satellites(View):

    def get(self, request):
        # actuate_sats()
        satellites = Satellite.objects.all().order_by('id')
        # tables for unique dates extraction (for template)
        dates = []
        uniq_dates = []
        # get history of one satellite (since data is collected for all the
        # satellites) - all satellites will have the same dates
        if satellites:
            example_sat = satellites[0]
            history = SatHistory.objects.filter(name=example_sat.name)
            # get all dates in the history as strings
            for hist_date in history:
                dates.append(hist_date.date.date().isoformat())
            # get unique dates
            for date in dates:
                if date not in uniq_dates:
                    uniq_dates.append(date)
            uniq_dates = uniq_dates[::-1]
        else:
            satellites = ''
            uniq_dates = ''

        context = {
            "satellites": satellites,
            "uniq_date": uniq_dates,
        }
        return render(request, "satellites.html", context)


class SatellitesInfo(View):
    def get(self, request, sat_id):
        satellite = Satellite.objects.get(pk=sat_id)
        sat_history = SatHistory.objects.filter(name=
                        satellite.name).order_by('-date')
        agency = satellite.agency
        try:
            personnel = satellite.personnel_set.all()
        except AttributeError:
            personnel = None
        context = {
            "satellite": satellite,
            "history": sat_history,
            "personnel": personnel,
            "agency": agency,
        }
        return render(request, "satellite_info.html", context)


class UpdateSatellites(UpdateView):
    model = Satellite
    template_name = "satellites_update_form.html"
    fields = ['agency']
    success_url = reverse_lazy('sat-all')


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
        try:
            satellites = agency.satellite_set.all()
            personnel = agency.personnel_set.all()
        except AttributeError:
            satellites = None
            personnel = None
        # sat_history.sort(key=operator.itemgetter('date'))
        context = {
            "agency": agency,
            "satellites": satellites,
            "personnel": personnel,
        }
        return render(request, "agency_info.html", context)


class AddSpaceAgency(CreateView):
    model = SpaceAgency
    template_name = "add_space_agency_form.html"
    fields = ["name", "acronym", "country", "launch_capable"]
    success_url = reverse_lazy("space-agencies")


class UpdateSpaceAgency(UpdateView):
    model = SpaceAgency
    template_name = "spaceagency_update_form.html"
    fields = ["name", "acronym", "country", "launch_capable"]
    success_url = reverse_lazy("space-agencies")


class DeleteSpaceAgency(DeleteView):
    model = SpaceAgency
    template_name = "spaceagency_confirm_delete.html"
    success_url = reverse_lazy("space-agencies")


class AllPersonnel(View):
    def get(self, request):
        # actuate_sats()
        # try:
        personnel = Personnel.objects.all()
        # except AttributeError:
        #     raise Http404
        context = {
            "personnel": personnel,
        }
        return render(request, "personnel.html", context)


class PersonnelInfo(View):
    def get(self, request, astr_id):
        personnel = Personnel.objects.get(pk=astr_id)
        agency = personnel.agency
        satellite = personnel.satellite
        context = {
            "personnel": personnel,
            "satellite": satellite,
            "agency": agency,
        }
        return render(request, "personnel_info.html", context)


class AddPersonnel(CreateView):
    model = Personnel
    template_name = "add_personnel_form.html"
    fields = ["first_name", "last_name", "agency", "satellite"]
    success_url = reverse_lazy('astr-all')


class UpdatePersonnel(UpdateView):
    model = Personnel
    template_name = "personnel_update_form.html"
    fields = ["first_name", "last_name", "agency", "satellite"]
    success_url = reverse_lazy("astr-all")


class DeletePersonnel(DeleteView):
    model = Personnel
    template_name = "personnel_confirm_delete.html"
    success_url = reverse_lazy("astr-all")


