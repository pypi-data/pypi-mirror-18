# Permission to use this file is granted in hearts/license.txt.

from datetime import date, datetime
from .datatype import Date, DateTime, Number, Text
from .bars import Bars
from .utils import Y


class Scale(object):
  '''
  Base class for various kinds of scale objects.
  '''

  @classmethod
  def infer(cls, layers, dimension):
    '''
    Infer's an appropriate default scale for a given sequence of
    :class:`.Series`.

    :param chart_series:
      A sequence of :class:`.Series` instances
    :param dimension:
      The dimension, :code:`X` or :code:`Y` of the data to infer for.
    :param data_type:
      The type of data contained in the series dimension.
    '''
    from .linear import Linear
    from .ordinal import Ordinal
    from .temporal import Temporal

    data_type = layers[0]._types[dimension]
    # Default Time scale is Temporal
    if data_type is Date:
      data_min = date.max
      data_max = date.min
      for series in layers:
        data_min = min(data_min, series.min(dimension))
        data_max = max(data_max, series.max(dimension))
      return Temporal(data_min, data_max)

    elif data_type is DateTime:
      data_min = datetime.max
      data_max = datetime.min
      for series in layers:
        data_min = min(data_min, series.min(dimension))
        data_max = max(data_max, series.max(dimension))
      return Temporal(data_min, data_max)

    elif data_type is Number:
      force_zero = False
      data_min = None
      data_max = None
      for series in layers:
        series_min = series.min(dimension)
        series_max = series.max(dimension)
        data_min = series_min if data_min is None else min(data_min, series_min)
        data_max = series_max if data_max is None else max(data_max, series_max)
        if isinstance(series, Bars) and dimension == Y:
          force_zero = True
      if force_zero:
        if data_min > 0: data_min = 0
        if data_max < 0: data_max = 0
      return Linear(data_min, data_max)

    elif data_type is Text:
      scale_values = None
      # First case: a single set of ordinal labels
      if len(layers) == 1:
        scale_values = layers[0].values(dimension)
      else:
        first_series = set(layers[0].values(dimension))
        data_series = [series.values(dimension) for series in layers]
        all_same = True
        for series in data_series:
          if set(series) != first_series:
            all_same = False
            break
        # Second case: multiple identical sets of ordinal labels
        if all_same:
          scale_values = layers[0].values(dimension)
        # Third case: multiple different sets of ordinal labels
        else:
          scale_values = sorted(list(set().union(*data_series)))
      return Ordinal(scale_values)

    raise ValueError(data_type)


  def contains(self, v):
    '''
    Return :code:`True` if a given value is contained within this scale's
    displayed domain.
    '''
    raise NotImplementedError


  def project(self, value, range_min, range_max):
    '''
    Project a value in this scale's domain to a target range.
    '''
    raise NotImplementedError


  def project_interval(self, value, range_min, range_max):
    '''
    Project a value in this scale's domain to an interval in the target
    range. This is used for places :class:`.Bars`.
    '''
    raise NotImplementedError


  def ticks(self):
    '''
    Generate a series of ticks for this scale.
    '''
    raise NotImplementedError


  def format_tick(self, value, i, count):
    '''
    Format ticks for display.

    This method is used as a default which will be ignored if the user
    provides a custom tick formatter to the axis.
    '''
    return str(value)
