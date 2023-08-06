#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

from diblogeo.util import _convert_to_km, _round, Point, Bounding, \
                           DistanceUnits, Angle, _calc_earth_radius, \
                           _point_usable, pass_dms, dms2dd, dd2dms

__all__ = ['Geo', 'calc_earth_radius', 'pass_dms', 'dms2dd', 'dd2dms', 'Point']

__version__ = '0.1.0rc1'
__author__ = 'Henrik Ankersø <henrik@diblo.dk'

class Geo(object):
    def __init__(self, point):
        """
        :Parameters:
          - `point: The list, tuple or string representing the 
                    latitude/longitude/altitude. Latitude and longitude
                    must be in decimal degrees or degrees minutes
                    seconds. Altitude must be specified as meter.
        """
        self._start_point = _point_usable(point)
        self._radius = None

    def __repr__(self):
        return "(%s, %s, %s)" %(self._start_point[0], \
                                self._start_point[1], \
                                self._start_point[2])

    def __iter__(self):
        for c in self._start_point:
            yield c

    def __len__(self):
        return len(self._start_point)

    def __getitem__(self, index):
        return self._start_point[index]

    def __getattr__(self, name):
        return getattr(Point(self._start_point), name)

    def _calc_radius(self):
        if self._radius is None:
            self._radius = _calc_earth_radius(self._start_point)
        return self._radius

    def set_start_point(self, point):
        """
        :Parameters:
          - `point: The list, tuple or string representing the 
                    latitude/longitude/altitude. Latitude and longitude
                    must be in decimal degrees or degrees minutes
                    seconds. Altitude must be specified as meter.
        """
        self._start_point = _point_usable(point)
        self._radius = None

    def bearing(self, point):
        """
        Calculates the bearing between two points.

        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                      cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

        :Parameters:
          - `point: The list, tuple or string representing the 
                    latitude/longitude/altitude. Latitude and longitude
                    must be in decimal degrees or degrees minutes
                    seconds. Altitude must be specified as meter.

        :Returns:
          The bearing in degrees

        :Returns Type:
          A instance of Angle

        :Source:
          https://gist.github.com/jeromer/2005586#file-compassbearing-py

        :Credit:
          https://gist.github.com/jeromer

        :Adapted by:
          https://github.com/Diblo
        """
        point = _point_usable(point)

        lat1 = math.radians(self._start_point[0])
        lat2 = math.radians(point[0])

        diffLong = math.radians(point[1] - self._start_point[1])
        cos_lat2 = math.cos(lat2)

        x = math.sin(diffLong) *cos_lat2
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * cos_lat2 * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        return Angle((math.degrees(initial_bearing) + 360) % 360)

    def distance(self, point):
        """
        Calculates the great circle distance between two points.
        The great circle distance is the shortest distance.
        This function uses the Haversine formula :
          - https://en.wikipedia.org/wiki/Haversine_formula

        :Parameters:
          - `point: The list, tuple or string representing the 
                    latitude/longitude/altitude. Latitude and longitude
                    must be in decimal degrees or degrees minutes
                    seconds. Altitude must be specified as meter.

        :Returns:
          The distance in kilometers

        :Returns Type:
          A instance of DistanceUnits

        :Source:
          https://gist.github.com/jeromer/1883777#file-orthodromicdistance-py

        :Credit:
          https://gist.github.com/jeromer

        :Adapted by:
          https://github.com/Diblo
        """
        point = _point_usable(point)

        diffLat = math.radians(point[0] - self._start_point[0])
        diffLon = math.radians(point[1] - self._start_point[1])

        lat1 = math.radians(self._start_point[0])
        lat2 = math.radians(point[0])

        a = math.sin(diffLat / 2) ** 2 + \
            math.sin(diffLon / 2) ** 2 * \
            math.cos(lat1) * math.cos(lat2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return DistanceUnits(c * self._calc_radius())

    def destination(self, bearing=0, distance=None, **kwargs):
        """

        :Parameters:
          - `bearing: The bearing in degrees
          - `distance: The distance in km
          - `kilometers: The distance in kilometers
          - `km: The distance in kilometers
          - `meters: The distance in meters
          - `m: The distance in meters
          - `miles: The distance in miles
          - `mi: The distance in miles
          - `feet: The distance in feets
          - `ft: The distance in feets
          - `nautical: The distance in nautical miles
          - `nm: The distance in nautical miles
          - `nmi: The distance in nautical miles

        :Returns:
          Latitude, longitude and altitude

        :Returns Type:
          A instance of Point
        """
        if len(kwargs):
            unit, distance = kwargs.popitem()
            distance = _convert_to_km(distance, unit)

        PI = math.pi
        lat1 = math.radians(self._start_point[0])
        lon1 = math.radians(self._start_point[1])
        bearing = math.radians(bearing)
        distance = distance / self._calc_radius()
        
        cos_lat1 = math.cos(lat1)
        sin_lat1 = math.sin(lat1)
        cos_distance = math.cos(distance)
        sin_distance = math.sin(distance)
     
        lat2 = math.asin(sin_lat1 * cos_distance + \
               cos_lat1 * sin_distance * math.cos(bearing))
        lon2 = lon1 + math.atan2(math.sin(bearing) * sin_distance * \
               cos_lat1, cos_distance - sin_lat1 * \
               math.sin(lat2))
        lon2 = math.fmod((lon2 + 3 * PI), (2 * PI)) - PI
     
        return Point((math.degrees(lat2), math.degrees(lon2), \
                     self._start_point[2]))

    def bounding(self, distance=None, **kwargs):
        '''
        Return bounding coordinates use for finding points within a
        distance
        
        :Parameters:
          - `distance: The distance in km
          - `kilometers: The distance in kilometers
          - `km: The distance in kilometers
          - `meters: The distance in meters
          - `m: The distance in meters
          - `miles: The distance in miles
          - `mi: The distance in miles
          - `feet: The distance in feets
          - `ft: The distance in feets
          - `nautical: The distance in nautical miles
          - `nm: The distance in nautical miles
          - `nmi: The distance in nautical miles
            
        :Returns:

        :Returns Type:
          A instance of Bounding
        '''

        if len(kwargs):
            unit, distance = kwargs.popitem()
            distance = _convert_to_km(distance, unit)

        PI = math.pi
        MIN_LAT = math.radians(-90)
        MAX_LAT = math.radians(90)
        #MIN_LON, MAX_LON = (-PI, PI)

        # angular distance in radians on a great circle
        rad_dist = float(distance) / self._calc_radius()
        rad_lat = math.radians(self._start_point[0])

        min_lat = rad_lat - rad_dist
        max_lat = rad_lat + rad_dist
        if min_lat > MIN_LAT and max_lat < MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(rad_lat))
            rad_lon = math.radians(self._start_point[1])

            min_lon = rad_lon - delta_lon
            if min_lon < -PI:
                min_lon += 2 * PI
                
            max_lon = rad_lon + delta_lon
            if max_lon > PI:
                max_lon -= 2 * PI

            return Bounding((_round(math.degrees(min_lat), 13), \
                             _round(math.degrees(min_lon), 13), \
                             _round(math.degrees(max_lat), 13), \
                             _round(math.degrees(max_lon), 13)))

        # a pole is within the distance
        return Bounding((_round(math.degrees(max(min_lat, MIN_LAT)), 13),\
                         -180, \
                         _round(math.degrees(min(max_lat, MAX_LAT)), 13), \
                         180))

def calc_earth_radius(point):
    """
    :Parameters:
      - `point: The list, tuple or string representing the 
                latitude/longitude/altitude. Latitude and longitude
                must be in decimal degrees or degrees minutes
                seconds. Altitude must be specified as meter.

    :Returns:
      The distance in kilometers

    :Returns Type:
      A instance of DistanceUnits
    """
    return DistanceUnits(_calc_earth_radius(_point_usable(point)))