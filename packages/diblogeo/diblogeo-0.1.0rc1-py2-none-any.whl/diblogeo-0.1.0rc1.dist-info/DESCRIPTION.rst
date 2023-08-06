Diblo Geo
__________

Diblo Geo is a Python 2 api for developer.

Diblo Geo makes it easy for Python developers to calculate coordinates and bearing across the globe.

Diblo Geo is tested against CPython 2.7.

`Development site <https://github.com/Diblo/diblogeo>`__.

© Diblo Geo contributors 2016 under the `The GNU General Public License v3.0 <https://github.com/Diblo/diblogeo/blob/master/LICENSE.txt>`__.

Installation
-----------------------------

Install using `pip <http://www.pip-installer.org/en/latest/>`__ with:

    pip install diblogeo

Or, `download a wheel or source archive from PyPI <https://pypi.python.org/pypi/diblogeo>`__.

Measuring Distances
-----------------------------
Example 1:

    >>> from diblogeo import Geo
    >>> distance = Geo((55.3303636516, 10.4466164796)) \
    ...            .distance((55.3706593849, 10.469825563))
    >>> print(distance)
    4.70941600331
    >>> print(distance.kilometers)
    4.71
    >>> print(distance.feet)
    15450.84

Example 2 (*Altitude 11.34 meters*):

    >>> from diblogeo import Geo
    >>> distance = Geo((55.3303636516, 10.4466164796, 11.34)) \
    ...            .distance((55.3706593849, 10.469825563, 11.34))
    >>> print(distance)
    4.71780808395
    >>> print(distance.kilometers)
    4.72
    >>> print(distance.feet)
    15478.37

Measuring Angles
-----------------------------
    >>> from diblogeo import Geo
    >>> bearing = Geo((55.3303636516, 10.4466164796)) \
    ...           .bearing((55.3706593849, 10.469825563))
    >>> print(bearing)
    18.1225041609
    >>> print(bearing.degrees)
    18.12
    >>> print(bearing.radians)
    0.316297366315

Projecting Destinations
-----------------------------
Example 1:

    >>> from diblogeo import Geo
    >>> point = Geo((55.3303636516, 10.4466164796))
    >>> point.destination(37.2, 3.2)
    (55.3533088458, 10.4772564424, 0)
    >>> point.destination(bearing=37.2, kilometers=3.2)
    (55.3533088458, 10.4772564424, 0)
    >>> point.destination(37.2, meters=3200)
    (55.3533088458, 10.4772564424, 0)

Example 2 *(Altitude 11.34 meters*):

    >>> from diblogeo import Geo
    >>> point = Geo((55.3303636516, 10.4466164796, 11.34))
    >>> point.destination(37.2, 3.2)
    (55.3532680374, 10.4772019082, 11.34)
    >>> point.destination(bearing=37.2, kilometers=3.2)
    (55.3532680374, 10.4772019082, 11.34)
    >>> point.destination(37.2, meters=3200)
    (55.3532680374, 10.4772019082, 11.34)

Calculate Earth's Radius:
-----------------------------
    >>> from diblogeo import calc_earth_radius
    >>> earth_radius = calc_earth_radius((55.3303636516, 10.4466164796, 11.34))
    >>> print(earth_radius)
    6375.05118755
    >>> print(earth_radius.kilometers)
    6375.05
    >>> print(earth_radius.miles)
    3961.27

More input and output methods:
--------------------------------
    >>> from diblogeo import Geo
    >>> location = Geo(("55° 19' 49.31\"", "10° 26' 47.82\"", 11.34)) \
    ...            .destination(37.2, miles=3.2)
    >>> print(location.latitude, location.longitude, location.altitude)
    (55.367221177288684, 10.495856496671713, 11.34)
    >>> print(location[0], location[1], location[2])
    (55.367221177288684, 10.495856496671713, 11.34)
    >>> print(location.dms)
    ((55, 22, 1.99624, 'N'), (10, 29, 45.08339, 'E'), 11.34)
    >>> print(location.dms.latitude, location.dms.longitude, location.altitude)
    ((55, 22, 1.99624, 'N'), (10, 29, 45.08339, 'E'), 11.34)

Locations/ Points Attributes
-----------------------------
The attributes can be used with `Geo` and `destination`.

Decimal Degrees:

* location, loc, dd
* latitude, lat
* longitude, lon
* elevations, altitude, alt

`location`, `loc` and `dd` return an instance of `_Point`

* [_Point].latitude, [_Point].lat
* [_Point].longitude, [_Point].lon
* [_Point].elevations, [_Point].altitude, [_Point].alt

Degrees Minutes Seconds:

* dms
* dms.latitude, dms.lat
* dms.longitude, dms.lon
* dms.elevations, dms.altitude, dms.alt

Unit of measurement
-----------------------------
The attributes can be used with `distance` and `calc_earth_radius`.
`Destination` supports all the units as distance argument.

* kilometers, km
* meters, m
* cm
* miles, mi
* feet, ft
* nautical, nm, nmi

Angle Units
-----------------------------
The attributes can be used with `bearing`.

* degrees, deg
* radians, rad


