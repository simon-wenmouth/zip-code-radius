#
#   Copyright 2015 Simon Wenmouth
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from math import degrees, radians, cos, sin, asin, sqrt, pi

MIN_LAT = radians(-90)  # -PI/2
MAX_LAT = radians(90)   #  PI/2
MIN_LON = radians(-180) # -PI
MAX_LON = radians(180)  #  PI

def bounding_box(lon, lat, distance, in_miles=True):
    """Calculate the bounding coordinates (lat_min, lon_min) and
    (lat_max, lon_max) which are opposite corners of a bounding
    rectangle (on the sphere) that completely contains the query
    circle.

    Args:
        lon (numeric)      : longitude in degrees
        lat (numeric)      : latitude in degrees
        distance (numeric) : the distance from the point
        in_miles (bool)    : True if the distance is in miles, False
            if the distance is in kilometers.

    Results:
        tuple (lat_min, lon_min, lat_max, lon_max)

        the lat/lon values are all in decimal degrees

    Acknowledgements:
    [1] http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates

    """
    R = 3956.0 if in_miles else 6371.0
    d = float(distance)/R
    lat, lon = map(radians, [lat, lon])
    lat_min = lat - d
    lat_max = lat + d
    if lat_min > MIN_LAT and lat_max < MAX_LAT:
        delta_lon = asin(sin(d) / cos(lat))
        lon_min = lon - delta_lon
        if lon_min < MIN_LON:
            lon_min += 2.0 * pi
        lon_max = lon + delta_lon
        if lon_max > MAX_LON:
            lon_max -= 2.0 * pi
    else:
        lat_min = max(lat_min, MIN_LAT)
        lat_max = max(lat_max, MAX_LAT)
        lon_min = MIN_LON
        lon_max = MAX_LON
    return (degrees(lat_min), degrees(lon_min), degrees(lat_max), degrees(lon_max))

def haversine(lon1, lat1, lon2, lat2, in_miles=True):
    """Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Args:
        lon1 (numeric)  : longitude in degrees of 1st point
        lat1 (numeric)  : latitude in degrees of 1st point
        lon2 (numeric)  : longitude in degrees of 2nd point
        lat2 (numeric)  : latitude in degrees of 2nd point
        in_miles (bool) : True if the unit of the result is miles,
                          otherwise False for kilometers.

    Results:
        distance (float): the distance between the two points

    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
    c = 2.0 * asin(sqrt(a))
    R = 3956.0 if in_miles else 6371.0
    return c * R

