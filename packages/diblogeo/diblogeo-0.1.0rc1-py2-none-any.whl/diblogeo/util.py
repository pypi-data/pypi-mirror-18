#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

__all__ = ['pass_dms', 'dms2dd', 'dd2dms', 'Point']

__version__ = '0.1.0rc1'
__author__ = 'Henrik Ankersø <henrik@diblo.dk'

convert_tabel = {
    'km': 1,
    'kilometers': 1,
    'm': 0.001,
    'meters': 0.001,
    'cm': 0.00001,
    'mi': 1.609344,
    'miles': 1.609344,
    'ft': 0.0003048,
    'feet': 0.0003048,
    'nm': 1.852,
    'nmi': 1.852,
    'nautical': 1.852
}

def _point_usable(point):
    if len(point) < 3:
        point += (0,)
    if type(point[0]) != float:
        return (dms2dd(*pass_dms(point[0])),
                dms2dd(*pass_dms(point[1])),
                point[2])
    return point

def _convert_to_km(value, unit):
    return value * convert_tabel[unit]

def _round(number, decimals=0):
    i = 10.0**decimals
    return int(number * i + 0.5) / i

def pass_dms(dms):
    dms = dms.replace(" ", "")
    degrees = 0
    for i in reversed(range(3)):
        try:
            degrees = int(dms[:i])
            break
        except ValueError:
            pass
    dms, d = dms.split('"')
    dms, s = dms.split("'")
    return (degrees, int(dms[-2:]), float(s), d)

def dms2dd(degrees, minutes, seconds, direction):
    dd = degrees + minutes / 60.0 + seconds / 3600.0
    direction = direction.lower()
    if direction == 's' or direction == 'w':
        dd *= -1
    return _round(dd, 13)

def dd2dms(deg, lat=True):
    degrees = int(deg)
    md = abs(deg - degrees) * 60
    minutes = int(md)
    sd = (md - minutes) * 60
    if lat:
        direction = 'N'
        if degrees < 0:
            direction = 'S'
    else:
        direction = 'E'
        if degrees < 0:
            direction = 'W'
    return (abs(degrees), minutes, _round(sd, 5), direction)

def _calc_earth_radius(point):
    lat = math.radians(point[0])
    r1 = 6378.137 # radius at equator in km
    r2 = 6356.752 # radius at pole in km
    radius = math.sqrt(((r1 ** 2 * math.cos(lat)) ** 2 + \
                       (r2 ** 2 * math.sin(lat)) ** 2) / \
                       ((r1 * math.cos(lat)) ** 2 + \
                       (r2 * math.sin(lat)) ** 2))
    return radius + point[2]

class _LocBase(object):
    def __init__(self, point):
        self._point = point

    def __repr__(self):
        return "(%s, %s, %s)" %(self._point[0], \
                                self._point[1], \
                                self._point[2])

    def __iter__(self):
        for c in self._point:
            yield c

    def __len__(self):
        return len(self._point)

    def __getitem__(self, index):
        return self._point[index]

class Point(_LocBase):
    def __getattr__(self, name):
        return getattr(_Point(self._point), name)

    @property
    def dd(self):
        return _Point(self._point)
    DD = dd
    loc = dd
    location = dd

    @property
    def dms(self):
        return _Point((dd2dms(self._point[0], True), \
                       dd2dms(self._point[1], False),
                       self._point[2]))
    DMS = dms

class _Point(_LocBase):
    @property
    def lat(self):
        return self._point[0]
    latitude = lat

    @property
    def lon(self):
        return self._point[1]
    longitude = lon

    @property
    def alt(self):
        return self._point[2]
    altitude = alt
    elevation = alt

class Bounding(_LocBase):
    def __repr__(self):
        return "(%s, %s, %s, %s)" %(self._point[0], \
                                    self._point[1], \
                                    self._point[2], \
                                    self._point[3])

    @property
    def min(self):
        return (self._point[0], self._point[1])
    minimum = min

    @property
    def min_lat(self):
        return self._point[0]
    min_latitude = min_lat
    minimum_lat = min_lat
    minimum_latitude = min_lat

    @property
    def min_lon(self):
        return self._point[1]
    min_longitude = min_lon
    minimum_lon = min_lon
    minimum_longitude = min_lon

    @property
    def max(self):
        return (self._point[2], self._point[3])
    maximum = max

    @property
    def max_lat(self):
        return self._point[2]
    max_latitude = max_lat
    maximum_lat = max_lat
    maximum_latitude = max_lat

    @property
    def max_lon(self):
        return self._point[3]
    max_longitude = max_lon
    maximum_lon = max_lon
    maximum_longitude = max_lon

class _FloatBase(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(_round(self._value, 2))

class DistanceUnits(_FloatBase):
    def __add__(self, value):
        return DistanceUnits(super(DistanceUnits, self).__add__(value))

    @property
    def km(self):
        return _round(self._value, 2)
    kilometers = km

    @property
    def m(self):
        return int(self._value / 0.001 + 0.5)
    meters = m

    @property
    def cm(self):
        return int(self._value / 0.00001 + 0.5)

    @property
    def mi(self):
        return _round(self._value / 1.609344, 2)
    miles = mi

    @property
    def ft(self):
        return _round(self._value / 0.0003048, 2)
    feet = ft

    @property
    def nm(self):
        return _round(self._value / 1.852, 2)
    nautical = nm
    nmi = nm

class Angle(_FloatBase):
    def __add__(self, value):
        return Angle(float.__add__(self, value))

    @property
    def deg(self):
        return _round(self._value, 2)
    degrees = deg

    @property
    def rad(self):
        return math.radians(self._value)
    radians = rad
