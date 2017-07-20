"""Satelite_Tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Sat_Track.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^map', Map.as_view(), name="map"),


    url(r'^personnel/(?P<astr_id>(\d)+)', PersonnelInfo.as_view(),
        name="astr-info"),


    url(r'^personnel', AllPersonnel.as_view(), name="astr-all"),

    url(r'^update_personnel/(?P<pk>(\d)+)', UpdatePersonnel.as_view(),
        name="astr-update"),


    url(r'^delete_personnel/(?P<pk>(\d)+)', DeletePersonnel.as_view(),
        name="astr-delete"),


    url(r'^add_personnel', AddPersonnel.as_view(), name="astr-add"),


    url(r'^satellites_list', SatellitesList.as_view(), name="REST-sat"),
    url(r'^history/$', History.as_view(), name="hist"),


    url(r'^satellites/(?P<sat_id>(\d)+)', SatellitesInfo.as_view(),
        name="sat-info"),


    url(r'^satellites', Satellites.as_view(), name="sat-all"),


    url(r'^update_satellites/(?P<pk>(\d)+)', UpdateSatellites.as_view(),
        name="update-satellites"),

    url(r'^space_agencies/(?P<agency_id>(\d)+)', AgencyInfo.as_view(),
        name="agency-info"),

    url(r'^space_agencies', SpaceAgencies.as_view(), name="space-agencies"),

    url(r'^add_space_agency', AddSpaceAgency.as_view(),
        name="add-space-agency"),


    url(r'^update_spaceagency/(?P<pk>(\d)+)', UpdateSpaceAgency.as_view(),
        name="update-space-agency"),


    url(r'^delete_spaceagency/(?P<pk>(\d)+)', DeleteSpaceAgency.as_view(),
        name="delete-space-agency"),
]
