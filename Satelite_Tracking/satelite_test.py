
from pyorbital.orbital import Orbital
from datetime import datetime
from pyorbital import tlefile
import requests
import re

# r_string = requests.get('http://celestrak.com/NORAD/elements/noaa.txt')
# r_filtered = r_string.text.split("\n")
#
# # every third element - satellite names in TLE
# r_filtered = r_filtered[0::3]
#
# sat_name = []
# for string in r_filtered:
#     sat_name.append(string.rstrip())
#     # print(string.rstrip())
# # tle = tlefile.read('RadarSat-2')
# # tle.inclination
#
#
# regex = re.compile("\w")
# for name in sat_name:
#     result = re.findall(regex, name)
#     print(result)

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

for name in SAT_NAME:
    try:
        orb = Orbital(name)
        now = datetime.utcnow()
        # Get normalized position and velocity of the satellite:
        normal_position = orb.get_position(now)
        # Get longitude, latitude and altitude of the satellite:
        geo_position = orb.get_lonlatalt(now)
        print("{} - {}".format(name, geo_position))
    except (KeyError, NotImplementedError):
        print('No satellite name: {}'.format(name))




        #
        #
        #
        #
        #
        # r_string = requests.get('http://celestrak.com/NORAD/elements/noaa.txt')
        # r_filtered = r_string.text.split(str="", num=r_string.count(str))
        #
        # # every third element - satellite names in TLE
        # r_filtered = r_filtered[0::3]
        #
        #
        #
        #
        # orb = Orbital("NOAA 15 [B]")
        # now = datetime.utcnow()
        # # Get longitude, latitude and altitude of the satellite:
        # geo_position = orb.get_lonlatalt(now)
        #
        #
        # # sateite = Category.objects.get(slug=slug)
        # # # nazwy klas czy nazwy atrybutow ? -> check!
        # # # products = Product.objects.filter(productcategory__category__slug=slug)
        # # products = Product.objects.filter(categories__slug=slug)
        #


