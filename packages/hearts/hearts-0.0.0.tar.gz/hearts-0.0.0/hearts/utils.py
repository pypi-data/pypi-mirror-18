# Permission to use this file is granted in hearts/license.txt.

from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal


# Shorthand
ZERO = Decimal('0')
NINE_PLACES = Decimal('1e-9')

#: X data dimension index
X = 0

#: Y data dimension index
Y = 1

#: Z data dimension index
Z = 2


DIMENSION_NAMES = ['X', 'Y', 'Z']

#: Data structure for representing margins or other CSS-edge like properties
Box = namedtuple('Box', ['top', 'right', 'bottom', 'left'])

#: Data structure for a single series data point
Datum = namedtuple('Datum', ['i', 'x', 'y', 'z', 'row'])

#: Dummy object used in place of a series when rendering legends for categories
DummySeries = namedtuple('DummySeries', ['name'])

